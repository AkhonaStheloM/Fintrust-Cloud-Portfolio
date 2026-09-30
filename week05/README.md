# FinTrust Week 05 AWS Architecture Design

## Overview

For Week 05, I designed a proposed AWS network and traffic routing layout for the FinTrust Bank SA scenario. The work is shown in four diagrams covering the VPC, hybrid connectivity, DNS and load balancer routing, and the combined CloudFront design.

The diagrams show the proposed design and the main decisions behind it. They are not proof that the AWS resources were deployed.

## Week 05 diagrams

### Day 1 VPC foundation

File: [`day01_target_architecture.png`](./day01_target_architecture.png)

For Day 1, I planned a VPC across two Availability Zones in the `af-south-1` region:

- VPC CIDR: `10.0.0.0/16`
- Availability Zone 1: `af-south-1a`
- Availability Zone 2: `af-south-1b`
- Public subnets for internet facing entry points
- Application subnets for application services
- Data subnets for transaction data and data layer workloads

I separated the subnet ranges by layer and spread them across both Availability Zones. This gives each layer a clearer boundary and avoids putting everything in one failure zone.

### Day 2 Hybrid connectivity

File: [`day02_architecture_design.png`](./day02_architecture_design.png)

The Day 2 diagram shows how existing FinTrust systems on premises could connect to AWS:

1. Systems on premises connect through either a VPN or AWS Direct Connect.
2. A Transit Gateway provides a central routing hub.
3. Network Firewall, route controls, and monitoring form a central inspection and control layer.
4. Separate Production, Development, Audit, and Shared Services VPCs receive logically controlled connectivity.

I kept the customer facing workloads, engineering environments, audit evidence, and shared services separate instead of treating AWS as one unrestricted network.

### Day 3 Route 53, CloudFront, and ALB routing

File: [`day3_route53.png`](./day3_route53.png)

The Day 3 diagram puts DNS, edge delivery, and application routing into one request flow:

1. Internet users send requests to the FinTrust domain.
2. Route 53 resolves the domain and represents health check based routing.
3. CloudFront provides HTTPS edge delivery and separates static and dynamic content paths.
4. A private S3 origin serves static portal assets through CloudFront access controls.
5. An Application Load Balancer handles dynamic application traffic.
6. ALB listener rules route `/api/*` requests to API targets and `/portal/*` requests to portal targets.
7. A weighted release example shows a controlled canary split of 10% and production traffic of 90%.

The percentages and routing values in the diagram are examples for learning. They are not live settings.

### Day 4 Combined CloudFront architecture

File: [`day04_cloudfront_architecture.png`](./day04_cloudfront_architecture.png)

The Day 4 diagram brings the CloudFront request flow together with the VPC and hybrid connectivity context:

1. Internet users enter through Route 53, which represents hosted zone resolution, health checks, TTL, and weighted routing.
2. CloudFront provides HTTPS edge delivery with Origin Access Control enabled.
3. Static portal assets are served from a private S3 bucket with public access blocked.
4. Dynamic requests are forwarded to the Application Load Balancer.
5. ALB listener rules direct `/api/*` traffic to API targets and `/portal/*` traffic to portal targets.
6. The target groups connect to application workloads inside the FinTrust VPC spanning two Availability Zones.
7. NAT gateways, security group flow, Transit Gateway, and connectivity to systems on premises are shown as supporting network context.

This helped me show how the edge, application routing, network segmentation, and hybrid connectivity fit together. It is still a proposed design, not deployment evidence.

## Key design decisions

### Two Availability Zones

I used two Availability Zones so the design is not dependent on one failure zone.

### Layered subnet separation

I separated the public, application, and data layers into different subnet groups. This makes the routing and access decisions easier to see. The diagrams do not claim that the route tables, Security Groups, network ACLs, or private endpoints were configured in AWS.

### Centralised hybrid connectivity

For Day 2, I used a central routing and inspection approach. Production, Development, Audit, and Shared Services are kept as separate logical environments.

### Separation of static and dynamic delivery

I separated the static portal assets from the dynamic application requests. The design uses CloudFront and a private S3 origin for static content, while the ALB handles the API and portal traffic.

### Controlled releases

The weighted routing example gives a canary release a smaller share of traffic before a wider rollout. The 10%/90% split is only an example and is not from a live deployment.

### Readability and documentation

I kept the diagrams simple, with short labels, clear boundaries, and arrows that show the direction of traffic. I used text labels for the AWS services so the diagrams stay readable.

## Evidence boundary

The diagrams in this folder are proposed designs only. They show what I planned, not what was deployed.

The following items were not confirmed in AWS:

- VPCs, subnets, route tables, or Availability Zones were provisioned.
- VPN, Direct Connect, Transit Gateway, Network Firewall, or monitoring controls were configured.
- Route 53 hosted zones or health checks were created.
- CloudFront, S3, ALB, target groups, or weighted routing were deployed.
- The illustrated architecture was tested with live traffic.
- The diagrams represent production approved or security approved architecture.

If I implement the design later, I will add separate evidence with the date, AWS region, resources, validation steps, and cost controls. For now, these files document proposed learning architectures only.

## Files in this folder

| File | Purpose |
|---|---|
| `day01_target_architecture.png` | Proposed VPC spanning two Availability Zones |
| `day02_architecture_design.png` | Proposed hybrid connectivity and central inspection design |
| `day3_route53.png` | Proposed Route 53, CloudFront, ALB, and weighted routing design |
| `day04_cloudfront_architecture.png` | Combined proposed CloudFront, VPC, ALB, and hybrid connectivity architecture |

## Accuracy note

This README explains the diagrams and the decisions behind them. I will add reflections and AWS validation only after I have completed and documented those activities.
