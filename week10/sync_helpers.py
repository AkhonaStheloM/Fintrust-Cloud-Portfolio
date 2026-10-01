MBPS_TO_BYTES = 1_000_000 / 8

def set_task_throttle(task_arn, bandwidth_mbps):
    ds = get_client('datasync')
    if bandwidth_mbps == 0:
        throttle = 0          # 0 = unlimited in DataSync API
    else:
        throttle = int(bandwidth_mbps * MBPS_TO_BYTES)

    ds.update_task(
        TaskArn=task_arn,
        Options={'BytesPerSecond': throttle}
    )
    label = f'{bandwidth_mbps} Mbps' if throttle else 'unlimited'
    print(f'Task throttle updated to {label} ({throttle} bytes/sec)')

# Lambda handler for EventBridge Scheduler
import os

def lambda_handler(event, context):
    task_arn = os.getenv('DATASYNC_TASK_ARN')
    mode     = event.get('mode', 'daytime')

    throttle_map = {
        'daytime':  500,   # 07:00-22:00 SAST
        'overnight': 9000, # 22:00-07:00 SAST
    }
    bandwidth = throttle_map.get(mode, 500)
    set_task_throttle(task_arn, bandwidth)
    return {'statusCode': 200, 'bandwidth_mbps': bandwidth, 'mode': mode}