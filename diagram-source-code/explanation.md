# Explanation of All 15 Diagrams

This document explains each diagram in the project package and links the design to the federated learning architecture described in the project.

## 1. System Architecture Diagram
### Diagram type
Mermaid architecture diagram

### Purpose
To show the overall structure of the system, including central server responsibilities and edge-device operations.

### Scope
The diagram spans presentation, API, federated learning coordination, edge processing, privacy and security, storage, and monitoring layers.

### Components explained
- Admin and System Operator interact with the dashboard.
- The Web Dashboard connects to the Backend API.
- The Authentication Service validates credentials and issues tokens.
- The Federated Learning Coordinator manages training rounds, eligible cohorts, and distribution of the global model.
- Edge devices maintain private local datasets and perform local training.
- Local training occurs inside a physical edge device, not in a central server.
- Privacy Protection, Differential Privacy, and Model Compression are applied before updates are sent.
- Secure Aggregation combines protected client updates and keeps individual contributions private.
- The Database stores metadata, model states, metrics, and logs.
- Monitoring gathers device telemetry and training metrics for dashboards.

### Data movement and relationships
The dashboard sends configuration and monitoring requests to the API. The API validates authentication and triggers coordinator actions. The coordinator broadcasts the global model to edge devices. Devices train locally and send protected updates. The server aggregates those updates and distributes the new model.

### Relevance
This diagram gives the project’s high-level view and is the first conceptual map for understanding the project.

### Assumptions
The project assumes a central coordinator, physical hardware devices, and privacy-preserving update transmission.

## 2. Entity Relationship Diagram (ERD)
### Diagram type
Mermaid ER diagram with Crow’s Foot notation

### Purpose
To describe the database structure needed for the system.

### Entities and keys
- Users: user_id (PK), role, login metadata
- AuthenticationSessions: session_id (PK), user_id (FK)
- EdgeDevices: device_id (PK), device_uuid, status, hardware attributes
- TrainingRounds: round_id (PK), target cohort size, status, timing metadata
- Models: model_id (PK), round_id (FK), version, validation metrics
- ModelUpdates: update_id (PK), round_id (FK), device_id (FK)
- DeviceMetrics: metric_id (PK), device_id (FK), round_id (FK)
- TrainingMetrics: metric_id (PK), round_id (FK), accuracy and privacy metrics
- AuditLogs: log_id (PK), user_id/device_id/round_id (FKs)

### Relationships
- One user may generate many audit logs and sessions.
- One training round may contain many model updates, metrics, and models.
- One device may participate in many rounds and produce many metrics.
- One model may be associated with many updates.

### Relevance
The ERD explains how the system stores user activity, device health, round status, model versions, and training outcomes.

### Assumptions
The database is normalized around training rounds, device participation, model state, and metrics rather than storing raw local data.

## 3. Data Flow Diagram Level 0
### Diagram type
Mermaid DFD context diagram

### Purpose
To show the whole federated learning system as a single process and its interactions with external entities.

### External entities
- Admin
- System Operator
- Physical Edge Devices

### Processes
- Process 0: Privacy-Preserving Federated Learning System

### Data flows
- Authentication requests and configuration commands from admin and operator
- Device registration and authentication from edge devices
- Resource telemetry from devices to the system
- Protected model updates sent to the coordinator
- Global model distribution back to devices
- Training status, reports, and performance summaries to users

### Important rule
Raw local datasets remain on edge devices and are never transmitted to the central server.

### Relevance
This is the top-level view used in system analysis and requirement validation.

## 4. Data Flow Diagram Level 1
### Diagram type
Mermaid DFD decomposition

### Processes
- P1: User Authentication and Device Registration
- P2: Federated Learning Configuration and Coordination
- P3: Local Model Training
- P4: Privacy Protection and Model Compression
- P5: Secure Aggregation and Global Model Update
- P6: Monitoring and Reporting

### Data stores
- D1 Users and Auth Sessions
- D2 Edge Device Registry
- D3 Training Rounds
- D4 Models
- D5 Model Updates
- D6 Device Metrics
- D7 Training Metrics
- D8 Audit Logs

### Why important
The diagram decomposes the single system process into operational flows that align with real federated learning engineering.

### Assumptions
Only a subset of the metadata is stored centrally; raw data remains private and local.

## 5. Data Flow Diagram Level 2
### Diagram type
Mermaid detailed DFD

### Purpose
To decompose the key training workflow into precise sub-processes.

### Sub-processes explained
- Receive Global Model
- Validate Training Configuration
- Select Eligible Edge Devices
- Distribute Global Model
- Perform Local Training
- Calculate Model Updates
- Apply Differential Privacy
- Perform Update Pruning and Sparsification
- Transmit Protected Updates
- Perform Secure Aggregation
- Aggregate Global Model
- Evaluate Model Performance
- Store Training Metrics
- Distribute Updated Global Model

### Data flow logic
The coordinator receives the current model, checks configuration, selects clients, and distributes the model. Devices train locally, compute updates, apply DP and compression, and upload protected updates. The server aggregates the updates and distributes a new global model.

### Relevance
This is the most detailed DFD for the training pipeline and should be used for design and viva explanations.

## 6. Use Case Diagram
### Diagram type
PlantUML use case diagram

### Actors
- Admin
- System Operator
- Registered Edge Device

### Use cases explained
- Login and authentication
- Manage users
- Register and authenticate edge devices
- Configure federated learning training
- Start a training round
- Select devices and distribute models
- Perform local training
- Apply differential privacy
- Compress updates
- Perform secure aggregation
- Aggregate the global model
- Monitor training and device health
- Generate reports

### Relationships
The diagram uses include, extend, and direct actor associations to show real system behavior. It avoids unnecessary use-case nesting.

### Relevance
This diagram captures user roles and system capabilities in a standard UML manner.

## 7. Class Diagram
### Diagram type
PlantUML class diagram

### Purpose
To represent the static software design of the system.

### Classes explained
- User, Admin, SystemOperator, AuthenticationService
- EdgeDevice, FLClient, LocalTrainer, Model
- DifferentialPrivacy, ModelCompressor, SecureAggregator, GlobalAggregator
- TrainingRound, ModelUpdate, DeviceMetrics, TrainingMetrics
- Dashboard, BackendAPI, DatabaseManager

### Relationships and multiplicity
The diagram demonstrates inheritance, association, composition, aggregation, and dependency. For example, Admin and SystemOperator inherit from User. One TrainingRound contains many ModelUpdates and DeviceMetrics. One FederatedLearningCoordinator manages many EdgeDevices and one training round. ModelUpdate objects are linked to differential privacy and compression processing.

### Why important
The class diagram shows how the software system is structured before implementation and ensures design clarity.

### Practical example
An admin configures a training round, the coordinator selects eligible devices, devices run local training, and the secure aggregator and global aggregator produce the next global model.

## 8. Sequence Diagram
### Diagram type
PlantUML sequence diagram

### Purpose
To show message flow during one federated learning round.

### Main interaction flow
1. Admin logs in.
2. Dashboard sends auth request.
3. Backend validates credentials.
4. Admin configures training parameters.
5. FL coordinator initializes the round.
6. Devices are selected and the global model is distributed.
7. Each device trains locally on private data.
8. DP is applied to updates.
9. Compression is applied.
10. Protected updates are sent to the secure aggregator.
11. Secure aggregation and global aggregation generate the next global model.
12. Metrics are stored and displayed to the dashboard.

### Alternative flow
The diagram includes an alt block for device unavailability, showing that the system can skip or retry a failed client.

### Relevance
This is the best diagram to explain runtime behavior during a viva or review.

## 9. Activity Diagram
### Diagram type
PlantUML activity diagram

### Purpose
To describe the complete training workflow from login to final result distribution.

### Workflow overview
The process starts with admin authentication. Training configuration is validated. The coordinator checks device availability, distributes the global model, and starts parallel local training on selected devices. Local updates are processed with differential privacy and model compression before secure aggregation. The new global model is evaluated, metrics are stored, and either a new round begins or final results are displayed.

### Decision points
- Are credentials valid?
- Are devices available and eligible?
- Is the stopping criterion satisfied?

### parallel execution
The diagram uses a fork to show that multiple edge devices train in parallel.

## 10. State Machine Diagram
### Diagram type
PlantUML state machine diagram

### Purpose
To show the lifecycle of a physical edge device.

### States
Unregistered, Registered, Authenticated, Available, SelectedForTraining, ReceivingGlobalModel, TrainingLocally, ApplyingDifferentialPrivacy, CompressingModelUpdate, UploadingModelUpdate, WaitingForNextRound, Offline, and Failed.

### Events and guards
Transitions are triggered by authentication, eligibility checks, network issues, and recovery events. Guards such as deviceOffline and recoveryFailed define realistic runtime behavior.

### Relevance
This diagram explains the behavior of edge devices across multiple training rounds and connectivity disruptions.

## 11. Component Diagram
### Diagram type
PlantUML component diagram

### Purpose
To show software components and their dependencies at the design level.

### Central server components
- Web Dashboard
- Backend API
- Authentication Service
- FL Coordinator
- Secure Aggregation Component
- Global Aggregation Component
- Monitoring Component
- Database

### Edge device components
- FL Client
- Local Training Component
- Privacy Protection Component
- Differential Privacy Component
- Model Compression Component

### Why it matters
This diagram identifies the modular system decomposition and shows how components communicate with each other.

## 12. Deployment Diagram
### Diagram type
PlantUML deployment diagram

### Purpose
To model the physical infrastructure and deployment layout.

### Nodes explained
- Admin Computer
- Web Browser
- Network Communication Layer
- Central FL Server
- Database Server
- Physical Edge Device 1, 2, 3, and additional edge devices

### Deployed artifacts
- Dashboard application
- Federated learning services
- Database storage
- Local datasets stored on devices

### Important rule
Raw local datasets remain on individual edge devices and are not moved to the central server.

## 13. Object Diagram
### Diagram type
PlantUML object diagram

### Purpose
To show a runtime snapshot of one training round.

### Objects
- FederatedLearningCoordinator
- TrainingRound
- GlobalModel
- EdgeDevice instances
- LocalModel instances
- ModelUpdate instances
- SecureAggregator
- GlobalAggregator

### Runtime content
The object diagram includes sample attribute values such as device identifiers, training round status, noise parameters, and update statistics.

### Why it matters
This diagram makes the round design concrete and helps translate classes into working system instances.

## 14. Package Diagram
### Diagram type
PlantUML package diagram

### Purpose
To show the logical organization of the software into modules.

### Packages
- presentation
- authentication
- api
- federated_learning
- edge_client
- local_training
- privacy
- secure_aggregation
- differential_privacy
- model_compression
- global_aggregation
- monitoring
- database
- common

### Dependency direction
The package structure avoids circular dependencies and reflects a layered design. Presentation depends on API, API depends on authentication and federated learning, and client-side packages depend on local training and privacy modules.

### Relevance
This helps in project documentation, team development, and modular implementation.

## 15. Communication Diagram
### Diagram type
PlantUML communication diagram

### Purpose
To show object-to-object interactions during a federated learning round.

### Objects involved
- Dashboard
- BackendAPI
- FLCoordinator
- EdgeDevice1
- EdgeDevice2
- LocalTrainer
- DifferentialPrivacy
- ModelCompressor
- SecureAggregator
- GlobalAggregator
- Database

### Message flow
The communication diagram follows the same round sequence as the sequence diagram. Authentication is validated, the round is configured, the global model is sent to devices, local updates are processed, and protected updates are aggregated before the global model is updated.

### Why it matters
This diagram highlights the interaction network between the main objects in the architecture.

## Summary
These fifteen diagrams collectively describe the full software design of the federated learning system. Together they cover system context, static structure, data storage, workflows, object behavior, deployment, and communication. They also preserve the essential architectural rule that local datasets remain on edge devices while updates are protected and transmitted securely.
