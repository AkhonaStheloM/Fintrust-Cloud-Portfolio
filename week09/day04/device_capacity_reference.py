import math

DEVICE_SPECS = {
    'Snowcone-HDD':              {'usable_tb': 8,       'description': 'Smallest, edge/disconnected'},
    'Snowcone-SSD':              {'usable_tb': 14,      'description': 'Snowcone with SSD'},
    'Snowball-Edge-Storage-Opt': {'usable_tb': 80,      'description': 'High-capacity storage migration'},
    'Snowball-Edge-Compute-Opt': {'usable_tb': 28,      'description': 'Edge compute and EC2-compatible'},
    'Snowmobile':                {'usable_tb': 100_000, 'description': 'Exabyte-scale, AWS truck required'},
}

SNOWMOBILE_THRESHOLD_TB = 10_000  # AWS recommendation: Snowmobile for more than 10PB

def plan_snow_transfer(data_size_tb, purpose='archive'):
    """
    Recommend a Snow device and quantity for a given data volume.
    """
    if data_size_tb >= SNOWMOBILE_THRESHOLD_TB:
        device = 'Snowmobile'
        count = math.ceil(data_size_tb / DEVICE_SPECS['Snowmobile']['usable_tb'])
        return {'device': device, 'count': count,
                'total_capacity_tb': count * DEVICE_SPECS['Snowmobile']['usable_tb']}

    # For archive use Storage Optimised; for compute use Compute Optimised
    device = 'Snowball-Edge-Storage-Opt' if purpose == 'archive' else 'Snowball-Edge-Compute-Opt'
    usable = DEVICE_SPECS[device]['usable_tb']
    count  = math.ceil(data_size_tb / usable)

    return {
        'device':           device,
        'count':            count,
        'total_capacity_tb': count * usable,
        'overhead_tb':      round(count * usable - data_size_tb, 1),
        'description':     DEVICE_SPECS[device]['description'],
    }

# FinTrust: 3PB regulatory archive to S3 Glacier Deep Archive
plan = plan_snow_transfer(3000, purpose='archive')
print(f'Device: {plan["device"]}')
print(f'Count:  {plan["count"]} devices')
print(f'Total capacity: {plan["total_capacity_tb"]:,} TB')
print(f'Overhead: {plan.get("overhead_tb", 0):,} TB unused')
