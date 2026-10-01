# AWS Cloud Concepts: Study Notes

## Purpose

These notes summarise the important concepts from the AWS Cloud Concepts study material used during Week 1. They are a learning summary. They do not claim that the services or designs described here were deployed in AWS.

## AWS Global Infrastructure

### Data centres

AWS data centres provide the physical foundation for cloud services. They host the computing, storage, networking, and other infrastructure used to deliver AWS services.

### Regions

An AWS Region is a separate geographic area that contains multiple Availability Zones. Regions help organisations choose where workloads and data should be hosted.

### Availability Zones

Availability Zones are separate locations within an AWS Region. Each Availability Zone contains one or more data centres and is designed to provide fault isolation. Availability Zones are connected by high bandwidth, low latency networking, which supports resilient architectures across more than one zone.

### Edge Locations

Edge Locations are points of presence positioned closer to end users. They help deliver content and services with lower latency, especially when used with content delivery services.

## Selecting an AWS Region

A Cloud Solutions Architect should evaluate the following before selecting a Region:

| Consideration | Why it matters |
|---|---|
| Compliance | Data residency, governance, and legal requirements may restrict where data can be stored or processed. |
| Latency | Placing workloads closer to users can improve response times and user experience. |
| Service availability | Services and features are not always available in every Region. |
| Pricing | Service prices can differ between Regions, so cost must be checked before a design is approved. |

Region selection is therefore a business, technical, compliance, and cost decision rather than a default setting.

## Cloud Computing and Its Benefits

Cloud computing provides on demand access to IT resources over the internet, usually with pay as you go pricing. Instead of buying and maintaining all physical infrastructure, an organisation can consume computing, storage, databases, networking, and other services as needed.

Important benefits include:

- Agility: resources can be provisioned and changed more quickly.
- Elasticity: capacity can increase or decrease to match demand.
- Cost savings: organisations can reduce large upfront infrastructure spending and pay for resources according to usage.
- Flexibility: teams can choose from a broad range of services and technologies.
- Global deployment: workloads and services can be placed in Regions and locations that support users and business requirements.
- Security support: AWS provides security capabilities and maintains security of the underlying cloud infrastructure, while customers remain responsible for their part of the environment.

## Shared Responsibility Model

The Shared Responsibility Model separates the responsibilities of AWS from the responsibilities of the customer.

| AWS responsibility | Customer responsibility |
|---|---|
| Security of the cloud | Security in the cloud |
| Physical data centres | Customer data |
| Regions, Availability Zones, and underlying infrastructure | Applications and application configuration |
| Hardware, networking infrastructure, and virtualisation | Identity and access management |
| Managed service infrastructure, according to the service used | Operating system and middleware where the chosen service requires customer management |
| Global infrastructure protection | Network and firewall configuration, encryption choices, and protection of data in transit |

The exact division changes according to the service model. Using a managed service can reduce infrastructure management, but it does not remove the customer's responsibility for data, access, configuration, and secure use of the service.

## Cloud Service Models

| Model | Main management responsibility |
|---|---|
| On premises | The organisation manages the complete environment, including facilities, hardware, networking, operating systems, applications, and data. |
| Infrastructure as a Service | The provider manages physical infrastructure and virtualisation. The customer manages areas such as the operating system, runtime, applications, and data. |
| Platform as a Service | The provider manages the infrastructure, operating system, middleware, and runtime. The customer focuses mainly on applications and data. |
| Software as a Service | The provider manages the application and the supporting platform and infrastructure. The customer manages its use of the software, data, access, and configuration available to it. |

Understanding these models helps an architect balance control, operational effort, speed, and responsibility.

## Cloud Deployment Models

- Public cloud: services are delivered through a cloud provider such as AWS.
- Private cloud: cloud infrastructure is dedicated to one organisation, often in an on premises environment.
- Hybrid cloud: public cloud and private cloud environments work together.

The appropriate model depends on factors such as compliance, existing systems, data sensitivity, operational capability, and the need for cloud flexibility.

## AWS Service Domains

AWS services are grouped into broad domains that help architects map business requirements to technical capabilities:

- Compute
- Storage
- Database
- Migration
- Network and Content Delivery
- Management and Governance
- Security, Identity and Compliance
- Messaging

A good architecture uses these domains together rather than selecting services in isolation. For example, an application may need compute, a database, storage, networking, identity controls, monitoring, and messaging as one connected design.

## AWS Cloud Economics and Value Proposition

Cloud economics focuses on the relationship between architecture decisions, resource usage, and business value. Key ideas include:

- Replacing large capital expenses with variable operating expenses.
- Reducing the need to purchase and maintain physical data centres.
- Scaling capacity to match demand instead of maintaining unnecessary fixed capacity.
- Using automation and managed services to reduce manual operational work.
- Comparing service pricing and Region pricing before selecting an architecture.
- Considering security, resilience, performance, and sustainability together with cost.

Cost optimisation is not simply choosing the cheapest service. It means meeting the required business and technical outcomes without paying for unnecessary capacity or features.

## AWS Well Architected Framework

The AWS Well Architected Framework provides six pillars for evaluating cloud designs:

1. Security: protect systems, data, identities, and access.
2. Reliability: recover from failures and continue operating as required.
3. Performance Efficiency: use resources efficiently and select suitable technologies.
4. Cost Optimisation: avoid unnecessary spending and manage resources responsibly.
5. Operational Excellence: operate, monitor, and improve workloads and processes.
6. Sustainability: use resources efficiently and reduce unnecessary environmental impact.

The pillars are connected. For example, improving reliability may require additional resources, while cost optimisation must not weaken security or the required level of resilience.

## AWS Design Principles

The study material highlights the following design principles:

- Design for scalability so the system can grow as demand increases.
- Treat resources as disposable where appropriate instead of relying on a single permanent server.
- Automate provisioning, testing, monitoring, and operational tasks.
- Use loose coupling so that one component can change or fail without bringing down the whole system.
- Prefer services over manually managed servers when the service meets the requirement.
- Use managed databases and other managed capabilities to reduce undifferentiated administration.
- Plan for increased data volumes and changing workload patterns.
- Remove single points of failure through redundancy and suitable fault isolation.
- Optimise for cost by matching capacity and service choices to actual requirements.
- Use caching when repeated access to stored or calculated data would improve performance and reduce unnecessary processing.
- Build security controls into the platform and make them easier to audit.

These principles are decision guides. They must still be balanced against the workload's requirements, constraints, risk, and budget.

## AWS Cloud Adoption Framework

The AWS Cloud Adoption Framework organises guidance into six perspectives:

### Business perspective

Connect cloud adoption to business outcomes, value, risk, and investment decisions.

### People perspective

Consider roles, skills, organisational change, training, and ways of working.

### Governance perspective

Define policies, controls, compliance processes, and decision structures.

### Platform perspective

Plan the technical foundation, landing zone, infrastructure, applications, and data platforms.

### Security perspective

Establish identity, protection, detection, response, and recovery capabilities.

### Operations perspective

Plan monitoring, service management, reliability, incident response, and continuous improvement.

The Business, People, and Governance perspectives focus mainly on business capabilities. The Platform, Security, and Operations perspectives focus mainly on technical capabilities. Together, they help an organisation prepare for the organisational and technical changes required for cloud adoption.

## Usefulness for a Cloud Solutions Architect

This information helps a Cloud Solutions Architect to:

- Translate business, compliance, latency, and cost requirements into Region and service decisions.
- Design workloads across suitable Availability Zones instead of relying on one location.
- Explain the security boundary between AWS and the customer.
- Select an appropriate service model based on the required level of control and operational effort.
- Compare public, private, and hybrid deployment options.
- Combine compute, storage, databases, networking, security, management, and messaging into a complete architecture.
- Evaluate designs using the six Well Architected pillars.
- Anticipate growth, failure, data volume, and operational change.
- Communicate architecture decisions to both technical and business stakeholders.
- Connect the technical solution to the people, governance, platform, security, and operations work needed for successful adoption.

## Study and Evidence Boundary

This file is a study summary based on the AWS Cloud Concepts PDF. It records concepts and design guidance for learning purposes. It is not evidence that AWS resources were created, configured, tested, or deployed. Practical evidence should be recorded separately using the relevant authorised screenshots, outputs, or activity records.
