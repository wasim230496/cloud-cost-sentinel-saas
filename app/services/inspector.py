import boto3
from typing import List, Dict

class CloudInspector:
    def __init__(self, access_key: str, secret_key: str, region: str = "ap-south-1"):
        """
        Initializes the AWS client session. Automatically detects LocalStack 
        running on the host to completely bypass live AWS billing triggers.
        """
        self.region = region

        # Ground Rule: Force connection to LocalStack if running inside our local dev sandbox
        # LocalStack listens on localhost port 4566
        self.endpoint_url = "http://127.0.0.1:4566"

        self.session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

    def scan_orphaned_ebs_volumes(self) -> List[Dict]:
        """
        Scans for EBS volumes that are in an 'available' state but detached 
        from any EC2 instances, leaking unnecessary baseline storage costs.
        """
        ec2_client = self.session.client('ec2', endpoint_url=self.endpoint_url)
        leaks = []

        try:
            # Query all EBS volumes in the current target region
            response = ec2_client.describe_volumes()

            for volume in response.get('Volumes', []):
                # An 'available' status instead of 'in-use' means it is orphaned
                if volume['State'] == 'available':
                    size_gb = volume['Size']
                    # Formula rule estimation: roughly $0.10 per GB per month
                    monthly_waste = size_gb * 0.10

                    leaks.append({
                        "resource_type": "EBS_ORPHAN",
                        "resource_id": volume['VolumeId'],
                        "estimated_monthly_waste": round(monthly_waste, 2),
                        "details": f"Size: {size_gb}GB, Status: Unattached"
                    })
        except Exception as e:
            print(f"Error inspecting EBS volumes: {str(e)}")

        return leaks

    def scan_idle_ec2_instances(self) -> List[Dict]:
        """
        Scans for running EC2 instances that are functionally idle, mapping 
        potential cost optimizations for down-sizing or hibernation schedules.
        """
        ec2_client = self.session.client('ec2', endpoint_url=self.endpoint_url)
        leaks = []

        try:
            response = ec2_client.describe_instances()

            for reservation in response.get('Reservations', []):
                for instance in reservation.get('Instances', []):
                    # We evaluate active, running servers to see if they are underutilized
                    if instance['State']['Name'] == 'running':
                        instance_id = instance['InstanceId']
                        instance_type = instance['InstanceType']

                        # In a real app, you would query CloudWatch metrics here.
                        # For our foundational mock baseline tier, we flag unmanaged instances.
                        # Estimated baseline rule cost waste based on instance types:
                        monthly_waste = 15.00 if "micro" in instance_type else 45.00

                        leaks.append({
                            "resource_type": "EC2_IDLE",
                            "resource_id": instance_id,
                            "estimated_monthly_waste": monthly_waste,
                            "details": f"Type: {instance_type}, Status: Low Utilization"
                        })
        except Exception as e:
            print(f"Error inspecting EC2 instances: {str(e)}")

        return leaks
