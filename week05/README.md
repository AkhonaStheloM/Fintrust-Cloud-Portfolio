# FinTrust Week 05: AWS Architecture Design

## Overview

Week 05 documents a proposed AWS network and traffic-routing architecture for the FinTrust Bank SA scenario. Four diagrams cover the VPC foundation, hybrid connectivity, DNS and application routing, and a combined CloudFront design.

This folder contains architecture documentation, not an executable implementation. The diagrams describe intended relationships between services. They do not establish that AWS resources were deployed, configured, or tested.

## Files

| File | Purpose |
|---|---|
| [`day01_target_architecture.png`](./day01_target_architecture.png) | Proposed VPC foundation across two Availability Zones, with public, application, and data subnet layers |
| [`day02_architecture_design.png`](./day02_architecture_design.png) | Proposed hybrid connectivity, central routing and inspection, and separate environment VPCs |
| [`day3_route53.png`](./day3_route53.png) | Proposed Route 53, CloudFront, S3, ALB, and weighted traffic-routing flow |
| [`day04_cloudfront_architecture.png`](./day04_cloudfront_architecture.png) | Combined edge delivery, application routing, VPC, and hybrid connectivity design |
| [`day04_cloudfront_architecture/README.md`](./day04_cloudfront_architecture/README.md) | Supporting narrative describing five source-image sections; the five named PNG files are not present in the supplied inventory |
| [`README.md`](./README.md) | Week-level overview, review workflow, and evidence boundaries |

The four root-level PNG files are the available diagram artifacts. The nested README’s statements about additional local images and upload status are not evidence that those images are included here.

## Architecture Walkthrough

### Day 1: VPC foundation

The documented design uses a VPC CIDR of `10.0.0.0/16` and two Availability Zones, `af-south-1a` and `af-south-1b`, in `af-south-1`.

Public, application, and data subnet groups separate internet-facing entry points, application services, and data workloads. Spreading these layers across two Availability Zones expresses a resilience objective, but does not verify failover behavior or availability.

`af-south-1` is retained as the diagram’s design value. It is not authorization to deploy there. Any lab discussion or implementation must use facilitator-approved Stockholm (`eu-north-1`), with regional details reviewed separately.

### Day 2: Hybrid connectivity

The hybrid design proposes connectivity from FinTrust systems on premises through VPN or AWS Direct Connect. A Transit Gateway provides a central routing hub, with Network Firewall, route controls, and monitoring represented as an inspection and control layer.

Production, Development, Audit, and Shared Services VPCs are separated logically. The diagram communicates intended network boundaries, not validated routing, firewall policies, or working connectivity.

### Day 3: DNS, edge delivery, and application routing

The documented request flow starts with Route 53 domain resolution and continues through CloudFront:

- Static portal assets use a private S3 origin with CloudFront access controls.
- Dynamic requests reach an Application Load Balancer.
- ALB listener rules direct `/api/*` and `/portal/*` requests to their respective targets.
- A 10% canary and 90% production split illustrates controlled releases.

The percentages are design examples, not live settings. DNS weighting and ALB request routing are distinct mechanisms; their presence in the design does not demonstrate a configured release workflow.

### Day 4: Combined architecture

The combined diagram brings Route 53, CloudFront, a private S3 origin, ALB routing, and application targets into the wider VPC context. Origin Access Control, blocked S3 public access, NAT gateways, security group flows, Transit Gateway, and on-premises connectivity are represented as proposed components.

This view connects the edge-delivery design to network segmentation and hybrid access. It does not prove that the illustrated controls are enforced in AWS.

## Local Review Workflow

### Prerequisites

- A local copy of `FinTrust-Cloud-Portfolio`
- A Markdown viewer or text editor
- An image viewer capable of opening PNG files

No AWS account, credentials, CLI configuration, packages, or runtime are required to review this folder.

From the repository root:

```sh
cd week05
ls -l
```

Open the four linked PNG files in an image viewer and review them in Day 1 through Day 4 order. Read the nested README as supporting narrative, while noting its missing image references.

**Inputs:** the FinTrust scenario, documented network ranges, proposed service relationships, and routing examples.

**Outputs:** four architecture diagrams and Markdown documentation. There is no local application, infrastructure code, deployment command, or test suite supplied for this week.

## Evidence and Deployment Boundaries

The repository does not provide AWS console evidence, deployment logs, live traffic results, or validation of provisioned resources. It also does not establish production approval, security approval, or guaranteed zero downtime.

Implementing this design would create potentially billable resources and could affect network access and traffic routing. Before any AWS action, validate the authorized account, facilitator-approved Stockholm region, permissions, service availability, quotas, expected costs, and cleanup responsibilities. The diagrams alone are not deployment instructions.