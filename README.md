# Contract Lifecycle Risk Manager

## 🛠️ Tech Stack & Architecture

### **Core Backend (Java Developer 1)**
* **Framework**: Spring Boot 3.2.0 (Java 17)
* **Database**: PostgreSQL with **Flyway** for schema versioning.
* **Caching**: **Redis** integration for high-performance contract retrieval.
* **Security**: Stateless **JWT** authentication with Spring Security.
* **API Docs**: Swagger/OpenAPI UI available at `/swagger-ui.html`.

### **AI & Data Layer**
* **AI Microservice**: Python (Flask) handling contract risk summarization.
* **Storage**: Hybrid approach using RDBMS (PostgreSQL) and Cache (Redis).

---

## 📊 Quality Assurance & Testing

To ensure the reliability of the **Contract Lifecycle Risk Manager**, the backend follows a strict testing protocol using **JUnit 5** and **Mockito**.

### **Day 11 Technical Milestone: Sign-off Ready**
* **Service Layer Coverage**: Achieved **100% Branch and Line coverage** on all core business logic.
* **Business Logic Verification**:
    * ✅ **Creation**: Validated successful contract persistence.
    * ✅ **Retrieval**: Verified both paginated list and ID-based lookups.
    * ✅ **Validation**: Tested input constraints (Null/Empty names and files).
    * ✅ **Exception Handling**: Confirmed `ResourceNotFound` and `InvalidContract` exceptions trigger correctly.
* **UX Support Logic**:
    * **Empty States**: API returns a valid empty `Page` object (`content: []`) instead of null, supporting frontend empty state illustrations.
    * **Error Boundaries**: Standardized JSON error schema implemented via `GlobalExceptionHandler` to prevent frontend crashes.

### **Test Execution**
- **Test Suite**: 10 Unit Tests
- **Tooling**: JaCoCo Maven Plugin
- **Run Tests**:
  ```powershell
  cd backend
  .\mvnw.cmd clean test

### **Day 11 Technical Milestone: Sign-off Ready**
![Service Coverage Report](./assets/coverage-report.png)

* **Service Layer Coverage**: Achieved **100% Branch and Line coverage**...