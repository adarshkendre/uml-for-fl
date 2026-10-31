# Explanation of All 15 Diagrams

This document explains each of the 15 diagrams for the project:
**Privacy-Preserving and Resource-Aware Federated Learning for Heterogeneous Edge Devices.**

---

## 1. System Architecture Diagram

**Diagram type:** Mermaid graph (top-to-bottom)

**Purpose:**
To show the overall structure of the system across five major layers.

**Main elements:**
- Presentation Layer: Admin and Web Dashboard
- API Layer: Backend API and Authentication Service
- FL Coordination Layer: FL Coordinator, Secure Aggregator, Global Aggregator
- Edge Device Layer: FL Client, Local Trainer, Privacy & Compression, Local Dataset
- Data Storage Layer: Central Database

**Important relationships:**
- Admin uses the Dashboard to configure training.
- The FL Coordinator distributes the global model to edge devices.
- Edge devices train locally, apply privacy and compression, and send masked updates back.
- The Secure Aggregator unmasks the cohort sum, and the Global Aggregator produces the next model.
- The Database stores models, metrics, and round records.

**Workflow:**
Admin logs in → configures and starts a round → Coordinator selects devices → devices train locally → privacy and compression are applied → masked updates are uploaded → server aggregates → updated model is stored and redistributed.

**Relevance:**
This is the primary high-level view of the project. It is the best diagram to begin a viva explanation.

---

## 2. Entity Relationship Diagram (ERD)

**Diagram type:** Mermaid erDiagram (Crow's Foot notation)

**Purpose:**
To describe the central database structure used by the system.

**Main entities:**
- **Users** (user_id PK, username, role, is_active)
- **EdgeDevices** (device_id PK, device_name, device_type, status)
- **TrainingRounds** (round_id PK, cohort_size, clipping_threshold, noise_multiplier, status)
- **Models** (model_id PK, round_id FK, version, validation_accuracy, validation_loss)
- **ModelUpdates** (update_id PK, round_id FK, device_id FK, dp_applied, secagg_masked)
- **DeviceMetrics** (metric_id PK, device_id FK, round_id FK, cpu_usage, ram_free_mb, battery_joules, admitted)
- **TrainingMetrics** (metric_id PK, round_id FK, global_accuracy, cumulative_epsilon, participating_devices)

**Important relationships:**
- One User configures many TrainingRounds.
- One TrainingRound produces many Models, ModelUpdates, DeviceMetrics, and TrainingMetrics.
- Each EdgeDevice submits ModelUpdates and reports DeviceMetrics per round.

**Relevance:**
This diagram explains how all system data — device health, training progress, privacy budget, and model versions — is organized and stored.

---

## 3. DFD Level 0 (Context Diagram)

**Diagram type:** Mermaid flowchart (Yourdon-DeMarco DFD approximation)

**Purpose:**
To show the complete system as one process and its interactions with external entities.

**Main elements:**
- External entities: Admin, System Operator, Physical Edge Devices
- Central process: Privacy-Preserving Federated Learning System (Process 0)

**Important data flows:**
- Admin sends login, training configuration, and device management commands.
- System Operator sends login and monitoring queries.
- Edge devices send device registration, resource telemetry, and masked model updates.
- The system sends auth tokens, status reports, global models, and training instructions.
- The local dataset on each edge device is explicitly shown as never transmitted.

**Relevance:**
This is the top-level system boundary diagram. It is useful for introducing the project scope to a new audience.

---

## 4. DFD Level 1

**Diagram type:** Mermaid flowchart (Yourdon-DeMarco DFD approximation)

**Purpose:**
To decompose the central system process into six major operational processes.

**Processes:**
- P1: Authentication and Device Registration
- P2: FL Coordination
- P3: Local Model Training
- P4: Privacy Protection and Compression
- P5: Secure Aggregation and Global Update
- P6: Monitoring and Reporting

**Data stores:**
- D1: Users and Devices
- D2: Training Rounds
- D3: Models
- D4: Metrics and Logs

**Workflow:**
Admin and devices authenticate through P1. Admin configures P2, which distributes the global model. Edge devices perform local training in P3. P4 applies privacy and compression. P5 aggregates updates and produces the new model. P6 sends monitoring data to users.

**Relevance:**
This diagram shows how the system's main responsibilities are divided and how data moves between them.

---

## 5. DFD Level 2

**Diagram type:** Mermaid flowchart (Yourdon-DeMarco DFD approximation)

**Purpose:**
To expand the key FL training processes (P2–P5) into detailed sub-processes.

**Sub-processes:**
- P2.1: Select eligible devices | P2.2: Distribute global model
- P3.1: Local SGD training | P3.2: Compute model update
- P4.1: Differential Privacy (clip + noise) | P4.2: Sparsify and quantize | P4.3: SecAgg masking
- P5.1: SecAgg unmask | P5.2: Aggregate global model | P5.3: Evaluate and store metrics

**Key point:**
The Local Dataset D_k flows only within the edge device sub-process and is never transmitted externally.

**Relevance:**
This is the most detailed DFD for the training pipeline and is ideal for viva explanations of how DP, compression, and secure aggregation fit together.

---

## 6. Use Case Diagram

**Diagram type:** PlantUML use case diagram (UML 2.5.1)

**Purpose:**
To describe user roles and the system capabilities available to each actor.

**Actors:**
- Admin
- System Operator
- Edge Device

**Use cases:**
- Login
- Register Edge Device
- Configure FL Training
- Start Training Round (includes: Select Devices and Distribute Model)
- Perform Local Training (includes: Apply Differential Privacy)
- Compress and Upload Update (extends: Aggregate Global Model)
- Monitor Training Progress
- View Model Performance

**Relevance:**
This diagram captures all meaningful interactions between human users, devices, and the system in one view.

---

## 7. Class Diagram

**Diagram type:** PlantUML class diagram (UML 2.5.1)

**Purpose:**
To represent the static software design of the system.

**Main classes:**

*Server-side:*
- **FLCoordinator** — manages rounds, selects devices, distributes and collects models
- **TrainingRound** — holds round parameters and status
- **GlobalAggregator** — computes the updated global model and tracks privacy budget
- **SecureAggregator** — unmasks cohort sum, handles dropouts via secret shares
- **Dashboard** — displays training progress and model performance

*Edge-side:*
- **EdgeDevice** — registers, sends telemetry, initiates training
- **FLClient** — receives model, executes round, uploads masked update
- **LocalTrainer** — runs local SGD on private dataset
- **DifferentialPrivacy** — clips updates and injects calibrated Gaussian noise
- **ModelCompressor** — applies sparsification, quantization, and SecAgg masking

**Important relationships:**
- FLCoordinator composes TrainingRound, GlobalAggregator, and SecureAggregator.
- FLClient composes LocalTrainer, DifferentialPrivacy, and ModelCompressor.
- FLCoordinator aggregates EdgeDevice instances.

**Relevance:**
This diagram shows how all software components are organized before implementation.

---

## 8. Sequence Diagram

**Diagram type:** PlantUML sequence diagram (UML 2.5.1)

**Purpose:**
To show the ordered message flow during one complete federated learning training round.

**Participants:**
Admin, Dashboard, FL Coordinator, Edge Device, Privacy & Compression, Secure Aggregator, Global Aggregator, Database

**Phases:**
1. Admin configures and starts the training round.
2. Coordinator selects an eligible device cohort.
3. Global model is broadcast to selected devices.
4. Each device trains locally on its private dataset (parallel).
5. Privacy and compression are applied; masked updates are uploaded.
6. Secure aggregation unmasks the cohort sum.
7. Global Aggregator computes the updated model and tracks privacy budget.
8. Metrics are stored; updated model is distributed; Dashboard is refreshed.

**Relevance:**
This is the most useful diagram for explaining runtime behavior during a viva or project review.

---

## 9. Activity Diagram

**Diagram type:** PlantUML activity diagram with swimlanes (UML 2.5.1)

**Purpose:**
To describe the complete training workflow from login to final model distribution.

**Swimlanes:**
- Admin
- Central FL Server
- Edge Devices

**Workflow:**
Admin logs in and configures training → server authenticates → global model initialized → for each round: server selects devices → global model distributed → devices train in parallel locally → DP, compression, and masking applied → masked updates uploaded → server unmasks and aggregates → model evaluated → metrics stored → model redistributed → repeat until stopping criteria met.

**Decision points:**
- Credentials valid?
- Enough devices available?
- Stopping criteria met?

**Relevance:**
This diagram gives a complete end-to-end picture of the workflow and is easy to follow during a viva explanation.

---

## 10. State Machine Diagram

**Diagram type:** PlantUML state machine diagram (UML 2.5.1)

**Purpose:**
To show the lifecycle of a physical edge device across registration, training, and failure recovery.

**States:**
- Unregistered → Registered → Authenticated → Available
- Available → TrainingLocally (when selected and resources eligible)
- TrainingLocally → WaitingForNextRound (after uploading update)
- WaitingForNextRound → Available (round complete) or re-selected → TrainingLocally
- Any state → Offline (connection lost)
- Offline → Authenticated (reconnect) or Registered (token expired) or [*] (shutdown)
- Failed → Unregistered (recovery) or [*] (permanent failure)

**Key internal actions in TrainingLocally:**
Run local SGD, apply DP (clip + noise), apply sparsification and masking, upload masked update.

**Relevance:**
This diagram explains the realistic behavior of edge devices including connectivity issues, round selection, and failure recovery.

---

## 11. Component Diagram

**Diagram type:** PlantUML component diagram (UML 2.5.1)

**Purpose:**
To show major software components and their dependencies at the architecture level.

**Central server components:**
Web Dashboard → Backend API → Auth Service, FL Coordinator → Secure Aggregator → Global Aggregator, Database

**Edge device components:**
FL Client → Local Trainer → Privacy & Compression (DP + Sparsification + Quantization) → SecAgg Masking → FL Client (masked upload)

**Inter-node communication:**
- FL Coordinator broadcasts global model to FL Client.
- FL Client uploads masked update to FL Coordinator.
- FL Client sends resource telemetry to FL Coordinator.

**Relevance:**
This diagram identifies modular decomposition and shows how server-side and edge-side software communicate.

---

## 12. Deployment Diagram

**Diagram type:** PlantUML deployment diagram (UML 2.5.1)

**Purpose:**
To model the physical infrastructure and deployment of the system.

**Nodes:**
- Admin Computer: Web Browser running Web Dashboard
- Central FL Server: Backend API, FL Coordinator, Global Aggregator, Secure Aggregator
- Database Server: Central Database
- Edge Device 1 (Raspberry Pi 4): FL Client, Local Trainer + DP + Compressor, Local Dataset D_1
- Edge Device 2 (Jetson Nano): FL Client, Local Trainer + DP + Compressor, Local Dataset D_2
- Edge Device N: FL Client + Local Stack, Local Dataset D_N

**Communication paths:**
Admin Computer ↔ Central FL Server: HTTPS
Central FL Server ↔ Database Server: TCP/IP
Central FL Server ↔ Each Edge Device: HTTPS (encrypted)

**Key rule:**
Raw local datasets remain on individual edge devices and are never transmitted.

**Relevance:**
This diagram maps the software system to real physical hardware and networking infrastructure.

---

## 13. Object Diagram

**Diagram type:** PlantUML object diagram (UML 2.5.1)

**Purpose:**
To show a concrete runtime snapshot during Training Round 1.

**Objects and key attribute values:**
- `coordinator1 : FLCoordinator` — cohortSize=3, dropoutMax=1
- `round1 : TrainingRound` — roundId=1, status="in_progress", clippingThreshold=1.0, noiseMultiplier=1.1
- `globalModel1 : Model` — version=3, validationAccuracy=0.842
- `device1 : EdgeDevice` — status="TrainingLocally" (Raspberry Pi 4)
- `device2 : EdgeDevice` — status="ApplyingPrivacy" (Jetson Nano)
- `device3 : EdgeDevice` — status="UploadingUpdate" (Generic SBC)
- `secAgg1 : SecureAggregator` — cohortSize=3, dropoutTolerance=1
- `globalAgg1 : GlobalAggregator` — activeCoordinates=6000

**Object links:**
Coordinator manages Round and distributes GlobalModel. Round includes all three Devices. SecAgg feeds cohort sum to GlobalAgg, which will produce the next global model.

**Relevance:**
This diagram makes the class design concrete with actual values and shows all three devices at different stages of the same training round.

---

## 14. Package Diagram

**Diagram type:** PlantUML package diagram (UML 2.5.1)

**Purpose:**
To show the logical organization of the software into modules.

**Server-side packages:**
- `presentation` — Dashboard
- `api` — Backend API, Auth Service
- `federated_learning` — FL Coordinator, Training Round, Device Selector
- `aggregation` — Global Aggregator, Secure Aggregator
- `database` — Database Manager

**Edge-device-side packages:**
- `edge_client` — FL Client, Local Trainer
- `privacy` — Differential Privacy, Model Compressor, SecAgg Masking

**Dependency direction:**
- `presentation` → `api` → `federated_learning` → `aggregation` → `database`
- `edge_client` → `privacy`
- No circular dependencies.

**Relevance:**
This diagram supports modular development and makes the separation of server-side and device-side responsibilities explicit.

---

## 15. Communication Diagram

**Diagram type:** PlantUML communication diagram (UML 2.5.1)

**Purpose:**
To show object-to-object interactions during one federated learning round with numbered messages.

**Objects:**
Dashboard, FL Coordinator, Edge Device, Local Trainer, Differential Privacy, Model Compressor, Secure Aggregator, Global Aggregator, Database

**Message sequence (numbered):**
1. Dashboard → Coordinator: configure and start round
2. Coordinator → DB: fetch global model → broadcast to Edge Device
3. Edge Device → LocalTrainer: train locally on D_k (data stays on device)
4. Edge Device → ModelCompressor: apply sparsification
5. Edge Device → DifferentialPrivacy: apply clip + noise
6. Edge Device → ModelCompressor: quantize and apply SecAgg mask
7. Edge Device → Coordinator: upload masked update y_k
8. Coordinator → SecureAggregator: unmask cohort sum
9. Coordinator → GlobalAggregator: aggregate → compute updated model + privacy budget
10. Coordinator → DB: store model and metrics, mark round complete
11. Coordinator → Edge Device: distribute updated model
12. Coordinator → Dashboard: async update (accuracy, epsilon, latency)

**Relevance:**
This diagram highlights the interaction network between the main objects and is consistent with the Sequence Diagram.

---

## Summary

These fifteen diagrams collectively cover the full software design of the federated learning system.

| # | Diagram | Type | Key Purpose |
|---|---------|------|-------------|
| 1 | System Architecture | Mermaid graph | Overall system layers |
| 2 | ER Diagram | Mermaid erDiagram | Database structure |
| 3 | DFD Level 0 | Mermaid flowchart | System boundary |
| 4 | DFD Level 1 | Mermaid flowchart | Major processes |
| 5 | DFD Level 2 | Mermaid flowchart | Detailed FL workflow |
| 6 | Use Case | PlantUML | User interactions |
| 7 | Class Diagram | PlantUML | Static software design |
| 8 | Sequence Diagram | PlantUML | Runtime message flow |
| 9 | Activity Diagram | PlantUML | Complete workflow |
| 10 | State Machine | PlantUML | Edge device lifecycle |
| 11 | Component Diagram | PlantUML | Software components |
| 12 | Deployment Diagram | PlantUML | Physical infrastructure |
| 13 | Object Diagram | PlantUML | Runtime snapshot |
| 14 | Package Diagram | PlantUML | Module organization |
| 15 | Communication Diagram | PlantUML | Object interactions |

All diagrams preserve the core project principles:
- **Local training** takes place on physical edge devices.
- **Raw data never leaves** the edge devices.
- **Differential Privacy** protects individual updates through adaptive clipping and Gaussian noise.
- **Secure Aggregation** hides individual contributions from the server.
- **Model pruning and sparsification** reduce communication overhead.
- The **FL Coordinator** manages training rounds and device selection.
- The **Global Aggregator** computes updated global models.
- The **Dashboard** monitors the complete system.
