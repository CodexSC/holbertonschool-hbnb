# HBnB Architecture - Quick Reference Guide

## 🏗️ Three-Layer Architecture Overview

```
┌─────────────────────────────────────────┐
│     PRESENTATION LAYER (API/Services)   │
│  - Handles HTTP requests/responses      │
│  - Input validation                     │
│  - Authentication                       │
└──────────────┬──────────────────────────┘
               │
               ├──> All requests go through Facade
               │
┌──────────────▼──────────────────────────┐
│         FACADE PATTERN (HBnBFacade)     │
│  - Single point of entry                │
│  - Simplifies communication             │
│  - Coordinates business logic           │
└──────────────┬──────────────────────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
┌────────────────┐  ┌────────────────────┐
│  BUSINESS      │  │  PERSISTENCE       │
│  LOGIC LAYER   │  │  LAYER             │
│  (Models)      │  │  (Repositories)    │
│                │  │                    │
│  - User        │  │  - UserRepository  │
│  - Place       │  │  - PlaceRepository │
│  - Review      │  │  - ReviewRepo      │
│  - Amenity     │  │  - AmenityRepo     │
│  - Business    │  │  - DatabaseManager │
│    Rules       │  │                    │
└────────────────┘  └────────────────────┘
```

---

## 📦 Layer Responsibilities

### Presentation Layer
✅ Receive HTTP requests  
✅ Validate input format  
✅ Authenticate users  
✅ Call facade methods  
✅ Format responses (JSON)  
✅ Return HTTP status codes  

**Components**: API endpoints, Services

---

### Business Logic Layer
✅ Define core entities (models)  
✅ Implement business rules  
✅ Validate data semantics  
✅ Orchestrate workflows  
✅ Ensure data integrity  

**Components**: User, Place, Review, Amenity, BusinessRules

---

### Persistence Layer
✅ Database operations (CRUD)  
✅ Manage connections  
✅ Execute queries  
✅ Handle transactions  
✅ Abstract database details  

**Components**: Repositories, DatabaseManager

---

## 🎯 Facade Pattern Benefits

| Benefit | Explanation |
|---------|-------------|
| **Simplification** | One interface instead of many classes |
| **Decoupling** | Layers don't know each other's internals |
| **Centralization** | Single point for logging, transactions |
| **Flexibility** | Change implementation without breaking API |

---

## 🔄 Request Flow

```
1. Client Request
   POST /api/places { title, price, owner_id }
   
2. API Layer
   - Validate JSON ✓
   - Authenticate ✓
   
3. Call Facade
   facade.createPlace(data)
   
4. Business Logic
   - Validate price > 0 ✓
   - Check owner exists ✓
   - Create Place object
   
5. Persistence
   - PlaceRepository.save(place)
   - Execute SQL INSERT
   
6. Response
   HTTP 201 Created
   { id, title, price, created_at }
```

---

## 📊 Core Entities

### User
```
Attributes: id, email, password, firstName, lastName
Relationships: owns Places, writes Reviews
Validations: unique email, password length
```

### Place
```
Attributes: id, title, description, price, location, ownerId
Relationships: belongs to User, has Reviews, has Amenities
Validations: price > 0, valid coordinates
```

### Review
```
Attributes: id, rating, comment, userId, placeId
Relationships: belongs to User, belongs to Place
Validations: rating 1-5, one per user per place
```

### Amenity
```
Attributes: id, name, description
Relationships: belongs to many Places
Validations: unique name
```

---

## 🔌 Communication Pathways

### API → Facade
- Direction: One-way (API calls Facade)
- Purpose: All presentation requests go through facade
- Example: `API.createPlace() → facade.createPlace()`

### Facade → Business Logic
- Direction: Facade coordinates models
- Purpose: Instantiate models, apply rules
- Example: `facade creates Place object, validates with BusinessRules`

### Facade → Persistence
- Direction: Facade delegates to repositories
- Purpose: Persist/retrieve data
- Example: `facade → PlaceRepository.save(place)`

### Model ↔ Model
- Direction: Bidirectional relationships
- Purpose: Domain model relationships
- Example: `User owns Places, Place has Reviews`

---

## ✅ Design Principles Applied

1. **Separation of Concerns**: Each layer has one responsibility
2. **Single Responsibility**: Each class has one purpose
3. **DRY**: Business logic centralized
4. **Dependency Inversion**: High-level doesn't depend on low-level
5. **Open/Closed**: Open for extension, closed for modification

---

## 🛠️ Implementation Guidelines

### DO ✅
- Always use facade for inter-layer communication
- Keep business logic in models, not in API
- Use repositories for all database access
- Validate in business logic layer
- Return meaningful error messages

### DON'T ❌
- Bypass the facade
- Write SQL in business logic
- Put validation in API layer
- Access database directly from models
- Mix layer responsibilities

---

## 📝 Code Examples

### Facade Method
```python
class HBnBFacade:
    def create_place(self, place_data):
        # 1. Validate
        if place_data['price'] <= 0:
            raise ValueError("Invalid price")
        
        # 2. Check dependencies
        owner = self.user_repo.findById(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")
        
        # 3. Create model
        place = Place(**place_data)
        
        # 4. Persist
        return self.place_repo.save(place)
```

### Repository Method
```python
class PlaceRepository:
    def save(self, place):
        query = "INSERT INTO places VALUES (?, ?, ?)"
        self.db.execute(query, [place.id, place.title, place.price])
        return place
```

### API Endpoint
```python
@app.route('/api/places', methods=['POST'])
def create_place():
    data = request.json
    try:
        place = facade.create_place(data)
        return jsonify(place.toDict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
```

---

## 🎓 Key Takeaways

1. **Three layers** separate concerns clearly
2. **Facade** is the gateway between layers
3. **Business logic** lives in the middle layer
4. **Repositories** abstract database operations
5. **Models** are rich objects with behavior
6. **Dependencies flow** in one direction (top → bottom)
7. **Each layer** is independently testable
8. **Architecture supports** scalability and maintainability

---

## 📚 Files Delivered

1. **hbnb_package_diagram.md** - Complete documentation with diagram
2. **hbnb_diagram.mermaid** - Standalone Mermaid diagram
3. **hbnb_quick_reference.md** - This quick reference guide

---

**Ready for implementation!** 🚀
