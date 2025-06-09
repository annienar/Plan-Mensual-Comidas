# Pantry Management System

## Overview
The Pantry Management System is the core feature that tracks ingredient availability and enables automatic shopping list generation. It bridges the gap between recipe ingredients and real-world inventory.

## Core Functionality

### 1. Ingredient Tracking
- **Stock Levels**: Track current quantity of each ingredient
- **Unit Standardization**: Normalize units across recipes and pantry
- **Expiration Dates**: Monitor freshness and prevent waste
- **Purchase History**: Track buying patterns and costs

### 2. Real-time Availability Checking
- **Recipe Analysis**: When adding recipes, immediately check pantry availability
- **Missing Ingredients**: Identify what needs to be purchased
- **Portion Scaling**: Adjust quantities based on available stock
- **Substitution Suggestions**: LLM-powered alternative ingredients

### 3. Automatic Stock Updates
- **Purchase Integration**: Update stock when shopping items are marked as bought
- **Usage Tracking**: Deduct ingredients when recipes are marked as "made"
- **Manual Adjustments**: Allow direct stock level modifications
- **Inventory Alerts**: Notify when items are running low

## Database Schema

### Enhanced Pantry Database (Alacena)
```
Pantry Item Properties:
├── Name (Text) - Ingredient name
├── Current Stock (Number) - Quantity available
├── Unit (Select) - Measurement unit
├── Minimum Stock (Number) - Low stock threshold
├── Purchase Date (Date) - When last purchased
├── Expiration Date (Date) - When item expires
├── Cost per Unit (Number) - Price tracking
├── Store/Supplier (Text) - Where to buy
├── Category (Select) - Organization (dairy, produce, etc.)
├── Notes (Rich Text) - Special storage instructions
└── Status (Select) - Available, Low, Expired, Out
```

### Ingredient-Pantry Relations
```
Enhanced Relations:
├── Ingredients → Pantry Items (Many-to-Many)
├── Recipes → Missing Items (Auto-calculated)
├── Shopping Lists → Pantry Items (Auto-generated)
└── Purchase History → Pantry Updates (Tracking)
```

## Workflow Integration

### Recipe Addition Workflow
1. **Recipe Processed** → LLM extracts ingredients
2. **Pantry Check** → System checks current stock levels
3. **Availability Analysis** → Determines what's available vs needed
4. **Missing Items** → Auto-adds to shopping list
5. **User Notification** → Shows availability status

### Shopping Workflow  
1. **Shopping List Generated** → Based on missing ingredients
2. **Items Purchased** → User marks items as bought in Notion
3. **Pantry Updated** → Stock levels automatically increased
4. **Recipes Updated** → Availability status refreshed

### Cooking Workflow
1. **Recipe Selected** → User chooses what to cook
2. **Availability Confirmed** → System verifies all ingredients available
3. **Recipe Completed** → User marks recipe as "made"
4. **Stock Deducted** → Ingredient quantities automatically reduced

## API Endpoints (To Be Implemented)

### Pantry Operations
```python
# Check ingredient availability for recipe
GET /api/pantry/check/{recipe_id}
Response: {
    "available": ["flour", "eggs"],
    "missing": ["milk", "butter"],
    "partial": {"sugar": {"needed": 2, "available": 1, "unit": "cups"}}
}

# Update stock levels
POST /api/pantry/update
Body: {
    "ingredient": "flour",
    "quantity": 5,
    "unit": "cups",
    "action": "add|set|subtract"
}

# Get low stock items
GET /api/pantry/low-stock
Response: {
    "items": [
        {"name": "milk", "current": 0.5, "minimum": 1, "unit": "liters"},
        {"name": "eggs", "current": 2, "minimum": 6, "unit": "pieces"}
    ]
}
```

### Shopping List Operations
```python
# Generate shopping list for recipe
POST /api/shopping/generate/{recipe_id}
Response: {
    "list_id": "shopping_123",
    "items": [
        {"ingredient": "milk", "quantity": 2, "unit": "cups", "store_section": "dairy"},
        {"ingredient": "butter", "quantity": 0.5, "unit": "cups", "store_section": "dairy"}
    ]
}

# Mark item as purchased
POST /api/shopping/purchase
Body: {
    "list_id": "shopping_123",
    "ingredient": "milk",
    "quantity_purchased": 2,
    "unit": "cups",
    "cost": 3.50
}
```

## LLM Integration Points

### Intelligent Ingredient Matching
```python
# LLM helps match recipe ingredients to pantry items
# Example: "1 cup all-purpose flour" → matches pantry item "flour"
# Handles variations: "AP flour", "plain flour", "harina"

Prompt Template:
"""
Match this recipe ingredient to available pantry items:
Recipe ingredient: "{ingredient_text}"
Available pantry: {pantry_items_list}

Return the best match or suggest if no match exists.
Consider synonyms, language variations, and common substitutions.
"""
```

### Smart Substitutions
```python
# When ingredients are missing, LLM suggests alternatives
Prompt Template:
"""
Recipe needs: {missing_ingredients}
Available in pantry: {available_ingredients}
Suggest substitutions that would work for this recipe type: {recipe_type}

Consider:
- Flavor compatibility
- Cooking properties
- Nutritional similarity
- Common substitution ratios
"""
```

### Quantity Optimization
```python
# LLM helps optimize purchase quantities
Prompt Template:
"""
Shopping list: {shopping_items}
Typical usage patterns: {usage_history}
Current pantry levels: {current_stock}

Optimize quantities to:
- Minimize waste
- Reduce shopping frequency
- Stay within budget: {budget}
- Consider shelf life of perishables
"""
```

## Implementation Phases

### Phase 1: Basic Pantry Tracking (Week 1)
- [ ] Create enhanced Pantry database schema in Notion
- [ ] Implement basic CRUD operations for pantry items
- [ ] Add stock level tracking
- [ ] Create simple availability checking

### Phase 2: Recipe Integration (Week 2)
- [ ] Implement recipe-to-pantry checking
- [ ] Add missing ingredient detection
- [ ] Create basic shopping list generation
- [ ] Integrate with recipe addition workflow

### Phase 3: Smart Features (Week 3)
- [ ] Add LLM-powered ingredient matching
- [ ] Implement substitution suggestions
- [ ] Add automatic stock updates
- [ ] Create low stock alerts

### Phase 4: Advanced Features (Week 4)
- [ ] Add expiration date tracking
- [ ] Implement cost tracking
- [ ] Add purchase history
- [ ] Create inventory analytics

## User Interface Considerations

### Pantry Dashboard
- **Stock Overview**: Visual indicators of stock levels
- **Low Stock Alerts**: Prominently displayed warnings
- **Quick Updates**: Easy stock adjustment controls
- **Category View**: Organized by ingredient types

### Recipe View Enhancements
- **Availability Indicators**: Green/yellow/red for each ingredient
- **Missing Items**: Clear list of what needs to be purchased
- **Alternative Suggestions**: LLM-powered substitutions
- **Cost Estimation**: Approximate meal cost based on pantry prices

### Shopping Interface
- **Auto-Generated Lists**: Based on selected recipes
- **Store Organization**: Grouped by store sections
- **Purchase Tracking**: Easy mark-as-bought interface
- **Cost Monitoring**: Budget tracking and spending alerts

## Success Metrics

### Functional Metrics
- **Availability Accuracy**: ≥95% correct ingredient status
- **Auto-Update Success**: ≥98% successful stock updates
- **Shopping List Accuracy**: ≥95% correct missing items
- **Substitution Quality**: ≥85% user acceptance of LLM suggestions

### User Experience Metrics
- **Recipe-to-Shopping Time**: <30 seconds workflow
- **Stock Update Frequency**: Daily active usage
- **Pantry Accuracy**: ≥95% user-reported accuracy
- **Feature Adoption**: ≥80% of users actively using pantry features

### Technical Metrics
- **Response Time**: <2 seconds for availability checks
- **Sync Reliability**: ≥99% successful Notion syncs
- **Data Consistency**: ≥99.9% accurate stock calculations
- **LLM Response Quality**: ≥90% helpful suggestions

## Future Enhancements

### Advanced Features
- **Meal Planning Integration**: Week/month planning with pantry optimization
- **Recipe Recommendations**: Based on available ingredients
- **Bulk Cooking**: Batch recipe suggestions for meal prep
- **Seasonal Optimization**: Ingredient suggestions based on season/availability

### Smart Integrations
- **Grocery Store APIs**: Real-time pricing and availability
- **Barcode Scanning**: Quick pantry updates via mobile
- **Smart Home Integration**: Connect with smart fridges/scales
- **Calendar Integration**: Plan shopping around schedules

## Notes & Considerations

### Technical Considerations
- **Unit Conversion**: Robust system for different measurement units
- **Language Support**: Spanish/English ingredient names
- **Data Validation**: Ensure stock levels never go negative
- **Conflict Resolution**: Handle concurrent updates gracefully

### Business Logic
- **Stock Thresholds**: Configurable minimum stock levels per ingredient
- **Expiration Handling**: Different strategies for different ingredient types
- **Cost Tracking**: Optional feature for budget-conscious users
- **Family Sharing**: Support for household pantry management

---

*This documentation will be updated as features are implemented and user feedback is collected.* 