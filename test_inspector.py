import boto3
from app.services.inspector import CloudInspector

def run_local_verification():
    print("Initializing LocalStack test targets...")

    # Connect directly to the local sandbox to seed test infrastructure
    local_ec2 = boto3.client('ec2', endpoint_url="http://127.0.0.1:4566", region_name="ap-south-1", aws_access_key_id="mock", aws_secret_access_key="mock")

    # Seed a mock 50GB unattached EBS volume inside our sandbox container
    print("Seeding an unattached 50GB test EBS Volume into LocalStack...")
    mock_volume = local_ec2.create_volume(
        AvailabilityZone="ap-south-1a",
        Size=50
    )
    volume_id = mock_volume['VolumeId']
    print(f"Mock Volume successfully created with ID: {volume_id}")

    # Now execution passes to our core SaaS script engine to verify detection rules
    print("\nExecuting CloudInspector scanning logic...")
    inspector = CloudInspector(access_key="mock", secret_key="mock", region="ap-south-1")

    ebs_leaks = inspector.scan_orphaned_ebs_volumes()

    print("\n--- SCAN RESULTS ---")
    print(f"Total Cost Leaks Found: {len(ebs_leaks)}")
    for leak in ebs_leaks:
        print(f"-> Detected [{leak['resource_type']}] ID: {leak['resource_id']} | Estimated Monthly Leak: ${leak['estimated_monthly_waste']}")

if __name__ == "__main__":
    run_local_verification()
