Monthly Meal Plan — Technical Documentation

Table of Contents

1. Overview
   1.1 Core Functionality
   1.2 System Components
   1.3 Key Features

2. Goals
   2.1 Primary Objectives
   2.2 Technical Goals
   2.3 Operational Goals
   2.4 Success Metrics
   2.5 Database Integration Goals

3. Database Structure
   3.1 Recetas (Recipes)
   3.2 Alacena (Pantry)
   3.3 Ingredientes (Recipe Ingredients)
   3.4 Lista de Compras (Shopping List)
   3.5 Database Relationships

4. Page Structure & Views
   4.1 Recipe Pages
   4.2 Database Views
   4.3 View-Specific Features
   4.4 Integration Points

5. Development Setup
   5.1 Environment Setup
   5.2 Dependencies
   5.3 Configuration
   5.4 Security & Permissions

6. Core Components
   6.1 Text Extraction Layer
   6.2 Recipe Processing Layer
   6.3 Notion Integration Layer
   6.4 Storage Layer
   6.5 Utils Layer

7. Operations
   7.1 Monitoring & Metrics
   7.2 Logging Strategy
   7.3 Error Handling
   7.4 Performance Considerations

8. Testing Strategy
   8.1 Test Categories
   8.2 Test Data
   8.3 Edge Cases
   8.4 Coverage Requirements

9. Development Process
   9.1 Code Conventions
   9.2 Git Workflow
   9.3 CI/CD Pipeline
   9.4 Release Process

10. Version Roadmap
    10.1 Current Version
    10.2 Planned Releases
    10.3 Feature Timeline

11. System Architecture
    11.1 Component Overview
    11.2 Data Flow
    11.3 Integration Points
    11.4 Security Considerations
    11.5 System Flow Diagrams

12. Future Enhancements
    12.1 Planned Features
    12.2 Technical Improvements
    12.3 Database Enhancements
    12.4 UI/UX Improvements

13. API Documentation
    13.1 Notion API Integration
        - Authentication & Authorization
        - Rate Limiting & Retry Strategy
        - Endpoint Documentation
        - API Versioning
        - Integration Testing

    13.2 Error Handling
        - Error Codes & Messages
        - Recovery Procedures
        - Notification Workflows
        - Logging Strategy

14. Deployment & Infrastructure
    14.1 Deployment Guide
        - Environment Setup
        - Container Configuration
        - Infrastructure Requirements
        - Scaling Guidelines
        - Production Checklist

    14.2 Data Management
        - Backup & Restore
        - Data Retention Policies
        - Disaster Recovery

15. Monitoring & Security
    15.1 Observability
        - Metrics Collection
        - Performance Monitoring
        - Alerting Configuration
        - SLA Definitions

    15.2 Security Framework
        - Access Control
        - Data Encryption
        - Security Best Practices
        - Audit Procedures

16. User & Contribution Guidelines
    16.1 User Documentation
        - End-user Guide
        - Troubleshooting
        - Common Workflows
        - FAQ

    16.2 Contributing
        - Contribution Workflow
        - Pull Request Process
        - Issue Management
        - Code Review Guidelines

17. Performance & Optimization
    17.1 Performance Strategy
        - Caching Implementation
        - Query Optimization
        - Resource Management
        - Performance Testing

    17.2 Internationalization
        - i18n Implementation
        - Language Support
        - Regional Formats
        - Character Encoding

18. Migration Considerations

    18.1 Data Migration Strategy
        - Existing Recipe Handling
          * Phased migration approach for existing recipes
          * Data transformation requirements
          * Quality validation checks
          * Rollback procedures
          * Progress tracking and reporting

        - Data Verification
          * Integrity checks
          * Format validation
          * Relationship verification
          * Content preservation

        - Contingency Planning
          * Rollback triggers and thresholds
          * Data recovery procedures
          * Manual intervention points
          * Communication protocols

    18.2 Integration Dependencies
        - API Requirements
          * Notion API version compatibility
          * OCR engine requirements
          * Third-party service dependencies
          * Version compatibility matrix

        - Quality Requirements
          * OCR accuracy thresholds
          * Language-specific requirements
          * Image quality minimums
          * Processing success criteria

    18.3 Performance Benchmarks
        - Volume Handling
          * Daily recipe processing capacity: 100 recipes/day
          * Peak usage handling: 20 concurrent processes
          * Batch operation limits: 50 recipes/batch
          * Response time requirements: < 5s per recipe

        - Resource Utilization
          * Memory usage limits
          * CPU utilization targets
          * Storage requirements
          * Network bandwidth needs

    18.4 Language Support Matrix
        - Current Languages
          * English (Primary)
          * Spanish (Primary)
          * Mixed-language handling
          * Character set support

        - Future Languages
          * Prioritized language additions
          * Translation requirements
          * Cultural format adaptations
          * Regional measurement systems

    18.5 Backup Strategy
        - Backup Schedule
          * Notion databases: Daily
          * Processed files: Weekly
          * Configuration: On change
          * Logs: Rolling 30-day retention

        - Recovery Procedures
          * Database restoration
          * File recovery
          * Configuration rollback
          * Service restoration

    18.6 User Interaction Framework
        - Notification System
          * Error notifications
          * Processing status updates
          * Stock level alerts
          * System maintenance notices

        - Manual Intervention
          * Quality review triggers
          * Correction workflows
          * Approval processes
          * Override mechanisms

    18.7 Security Framework
        - Data Privacy
          * Personal information handling
          * Access control levels
          * Data encryption requirements
          * Retention policies

        - Audit Requirements
          * Action logging
          * Change tracking
          * Access monitoring
          * Compliance reporting

    18.8 Monitoring Framework
        - Critical Metrics
          * Processing success rate
          * API response times
          * Error rates
          * Resource utilization

        - Alert Routing
          * Critical alerts: Immediate (SMS/Call)
          * Warning alerts: Email
          * Info alerts: Dashboard
          * Maintenance alerts: Scheduled digest

    18.9 Migration Readiness

        1. Pre-Migration Checklist
           - System State Documentation
             * Current database snapshots
             * Configuration backups
             * User permissions audit
             * Integration status verification

           - Environment Validation
             * Python 3.13 installation
             * Required system packages
             * Database access verification
             * API token validation

           - Data Preparation
             * Backup verification
             * Data integrity checks
             * Schema validation
             * Test data preparation

           - Resource Verification
             * Storage capacity check
             * Memory availability
             * CPU capacity
             * Network bandwidth

        2. Migration Procedure
           Phase 1: Preparation (Day 1)
           - Create full system backup
           - Verify all API tokens
           - Run environment validation
           - Prepare rollback points

           Phase 2: Core Migration (Day 2)
           - Migrate database schema
           - Update configuration files
           - Deploy new code version
           - Run initial validation

           Phase 3: Data Migration (Days 3-4)
           - Migrate recipe data
           - Update relationships
           - Verify data integrity
           - Run consistency checks

           Phase 4: Verification (Day 5)
           - Run full system tests
           - Verify all integrations
           - Check performance metrics
           - Validate backup systems

        3. Validation Points
           - Database Schema
             * Table structure matches specification
             * Indexes are properly created
             * Constraints are enforced
             * Relationships are valid

           - Data Integrity
             * All recipes migrated
             * Relationships preserved
             * No duplicate entries
             * Data quality maintained

           - System Performance
             * Response times within limits
             * Resource usage acceptable
             * No memory leaks
             * API limits respected

           - Integration Health
             * All APIs responding
             * Authentication working
             * Rate limits respected
             * Error handling functioning

        4. Rollback Procedures
           - Trigger Conditions
             * Data corruption detected
             * Performance degradation
             * Integration failures
             * Critical errors

           - Rollback Steps
             1. Stop all services
             2. Restore database backup
             3. Revert code changes
             4. Restore configuration
             5. Verify system state
             6. Resume services
             7. Notify stakeholders

           - Recovery Verification
             * Database consistency
             * Application functionality
             * Integration status
             * Performance metrics

        5. Communication Plan
           - Stakeholder Updates
             * Pre-migration briefing
             * Progress updates
             * Completion notification
             * Issue alerts

           - Technical Communication
             * Team coordination
             * Issue reporting
             * Status monitoring
             * Decision points

           - Documentation Updates
             * Migration logs
             * Change records
             * Issue tracking
             * Lesson learned

    18.10 Terminology Standardization
        - Recipe Processing Terms
          * "Recipe extraction" (not "recipe parsing")
          * "Ingredient normalization" (not "ingredient standardization")
          * "Recipe structure" (not "recipe format")
          * "Processing pipeline" (not "processing flow")

        - Technical Terms
          * "API integration" (not "API connection")
          * "Data validation" (not "data verification")
          * "Error handling" (not "error management")
          * "Performance optimization" (not "performance improvement")

        - Metric Standards
          * Processing time: seconds (s)
          * Memory usage: megabytes (MB)
          * Storage: gigabytes (GB)
          * Throughput: recipes per minute (rpm)

        - Version Format
          * Major.Minor.Patch (e.g., 1.4.8)
          * Date-based versions: YYYY-MM-DD
          * API versions: YYYY-MM-DD
          * Build numbers: YYYYMMDD.build_number

19. Feature Priorities

    19.1 Core Features (P0)
        1. Recipe Processing Engine
           Core Functionality:
           - PDF text extraction
             * Support for single and multi-page PDFs
             * Text layer extraction
             * Image-based PDF processing
             * PDF structure preservation
             * Implementation using pdfplumber and pdf2image
             ```python
             class PDFProcessor:
                 def __init__(self):
                     self.pdf_reader = PDFReader()
                     self.text_extractor = TextExtractor()
                     self.image_processor = ImageProcessor()

                 async def process_pdf(self, file_path: str) -> RecipeText:
                     if self._has_text_layer(file_path):
                         return await self.text_extractor.extract(file_path)
                     return await self.image_processor.extract(file_path)
             ```

           - Basic ingredient parsing
             * Ingredient line detection
             * Quantity extraction
             * Unit normalization
             * Ingredient name isolation
             * Implementation using regex and NLP
             ```python
             class IngredientParser:
                 def __init__(self):
                     self.quantity_pattern = r'(\d+(?:/\d+)?(?:\.\d+)?)\s*([a-zA-Z]+)?'
                     self.unit_normalizer = UnitNormalizer()

                 def parse_line(self, line: str) -> Ingredient:
                     quantity, unit = self._extract_quantity_unit(line)
                     name = self._extract_ingredient_name(line)
                     return Ingredient(
                         name=name,
                         quantity=quantity,
                         unit=self.unit_normalizer.normalize(unit)
                     )
             ```

           - Recipe structure detection
             * Section identification (ingredients, instructions, metadata)
             * Hierarchical structure parsing
             * Format normalization
             * Implementation using pattern matching
             ```python
             class StructureDetector:
                 def __init__(self):
                     self.section_patterns = {
                         'ingredients': r'(?i)ingredients?:?',
                         'instructions': r'(?i)(instructions?|directions?|method):?',
                         'metadata': r'(?i)(prep time|cook time|servings|yield):?'
                     }

                 def detect_sections(self, text: str) -> RecipeStructure:
                     sections = {}
                     for section_type, pattern in self.section_patterns.items():
                         sections[section_type] = self._extract_section(text, pattern)
                     return RecipeStructure(**sections)
             ```

           - Essential metadata extraction
             * Cooking time
             * Serving size
             * Difficulty level
             * Source attribution
             * Implementation using metadata extractors
             ```python
             class MetadataExtractor:
                 def __init__(self):
                     self.time_pattern = r'(\d+)\s*(min|hour)'
                     self.servings_pattern = r'serves?\s*(\d+)'
                     self.difficulty_keywords = {
                         'easy': 1,
                         'medium': 2,
                         'hard': 3
                     }

                 def extract_metadata(self, text: str) -> RecipeMetadata:
                     return RecipeMetadata(
                         cook_time=self._extract_time(text),
                         servings=self._extract_servings(text),
                         difficulty=self._assess_difficulty(text),
                         source=self._extract_source(text)
                     )
             ```

           Testing Requirements:
           - Unit tests for each component
           - Integration tests for full pipeline
           - Performance benchmarks
           - Error case coverage

           Success Criteria:
           - 90% accuracy in basic recipe parsing
           - < 5 second processing time per recipe
           - Correct section identification
           - Accurate ingredient parsing

        2. Notion Integration
           Core Functionality:
           - Database creation
             * Schema definition
             * Property configuration
             * Relationship setup
             * Implementation using Notion API
             ```python
             class NotionDatabaseManager:
                 def __init__(self, notion_client: NotionClient):
                     self.client = notion_client
                     self.schema = self._load_schema()

                 async def create_database(self, parent_id: str) -> str:
                     properties = {
                         "Name": {"title": {}},
                         "Portions": {"number": {}},
                         "Time": {"rich_text": {}},
                         "Ingredients": {"relation": {
                             "database_id": self.ingredient_db_id
                         }},
                         "Tags": {"multi_select": {
                             "options": self._get_default_tags()
                         }}
                     }
                     return await self.client.create_database(
                         parent_id=parent_id,
                         properties=properties
                     )
             ```

           - Recipe page creation
             * Content formatting
             * Property mapping
             * Image handling
             * Implementation using page templates
             ```python
             class RecipePageCreator:
                 def __init__(self, notion_client: NotionClient):
                     self.client = notion_client
                     self.template = self._load_template()

                 async def create_recipe_page(self, recipe: Recipe) -> str:
                     content_blocks = self._create_content_blocks(recipe)
                     properties = self._map_properties(recipe)

                     return await self.client.create_page(
                         parent={"database_id": self.recipe_db_id},
                         properties=properties,
                         children=content_blocks
                     )
             ```

           - Basic property mapping
             * Data type conversion
             * Validation rules
             * Default values
             * Implementation using property mappers
             ```python
             class PropertyMapper:
                 def __init__(self):
                     self.type_converters = {
                         "number": self._convert_number,
                         "select": self._convert_select,
                         "multi_select": self._convert_multi_select,
                         "date": self._convert_date
                     }

                 def map_properties(self, recipe: Recipe) -> Dict[str, Any]:
                     return {
                         name: self.type_converters[prop_type](value)
                         for name, (prop_type, value) in recipe.properties.items()
                     }
             ```

           - Error handling
             * Rate limit handling
             * Retry logic
             * Error recovery
             * Implementation using error handlers
             ```python
             class NotionErrorHandler:
                 def __init__(self):
                     self.retry_config = {
                         "max_attempts": 3,
                         "initial_delay": 1,
                         "max_delay": 10,
                         "backoff_factor": 2
                     }

                 @retry(**retry_config)
                 async def handle_request(self, func: Callable, *args, **kwargs):
                     try:
                         return await func(*args, **kwargs)
                     except APIResponseError as e:
                         if e.code == "rate_limited":
                             raise RetryableError(e)
                         raise
             ```

           Testing Requirements:
           - API integration tests
           - Rate limit testing
           - Error scenario coverage
           - Data consistency validation

           Success Criteria:
           - 100% successful page creation
           - < 2 second API response time
           - Zero data loss during transfer
           - Proper error recovery

        3. Data Validation
           Core Functionality:
           - Input validation
             * File format verification
             * Content structure validation
             * Character encoding checks
             * Implementation using validators
             ```python
             class InputValidator:
                 def __init__(self):
                     self.supported_formats = {'.pdf', '.txt', '.jpg', '.png'}
                     self.min_file_size = 100  # bytes
                     self.max_file_size = 10 * 1024 * 1024  # 10MB

                 async def validate_input(self, file_path: str) -> bool:
                     if not self._check_format(file_path):
                         raise UnsupportedFormatError(file_path)
                     if not self._check_file_size(file_path):
                         raise FileSizeError(file_path)
                     return await self._validate_content(file_path)
             ```

           - Format verification
             * Schema compliance
             * Data type checking
             * Relationship validation
             * Implementation using schema validators
             ```python
             class SchemaValidator:
                 def __init__(self):
                     self.schema = self._load_schema()
                     self.validators = {
                         'string': self._validate_string,
                         'number': self._validate_number,
                         'array': self._validate_array,
                         'object': self._validate_object
                     }

                 def validate_schema(self, data: Dict[str, Any]) -> bool:
                     for field, rules in self.schema.items():
                         if not self.validators[rules['type']](data.get(field)):
                             raise SchemaValidationError(field)
                     return True
             ```

           - Required field checking
             * Mandatory field validation
             * Default value handling
             * Cross-field validation
             * Implementation using field validators
             ```python
             class FieldValidator:
                 def __init__(self):
                     self.required_fields = {
                         'title': str,
                         'ingredients': list,
                         'instructions': list
                     }
                     self.default_values = self._load_defaults()

                 def validate_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
                     validated = {}
                     for field, field_type in self.required_fields.items():
                         value = data.get(field, self.default_values.get(field))
                         if value is None:
                             raise MissingFieldError(field)
                         if not isinstance(value, field_type):
                             raise FieldTypeError(field, field_type)
                         validated[field] = value
                     return validated
             ```

           - Relationship validation
             * Foreign key checks
             * Circular reference detection
             * Integrity constraints
             * Implementation using relationship validators
             ```python
             class RelationshipValidator:
                 def __init__(self, notion_client: NotionClient):
                     self.client = notion_client
                     self.cache = RelationshipCache()

                 async def validate_relationships(self, recipe: Recipe) -> bool:
                     # Validate ingredient relationships
                     for ingredient in recipe.ingredients:
                         if not await self._validate_ingredient_exists(ingredient):
                             raise InvalidRelationshipError(ingredient)

                     # Validate category relationships
                     if not await self._validate_category_exists(recipe.category):
                         raise InvalidCategoryError(recipe.category)

                     return True
             ```

           Testing Requirements:
           - Comprehensive validation tests
           - Edge case coverage
           - Performance impact testing
           - Error message verification

           Success Criteria:
           - Zero data corruption incidents
           - 100% validation coverage
           - < 1 second validation time
           - Clear error messages

    19.2 Enhanced Features (P1)
        1. Advanced Recipe Processing
           - Image OCR support
           - Multi-language parsing
           - Complex format handling
           - Style preservation
           Priority: High
           Dependencies: Core Recipe Processing
           Success Criteria: 95% accuracy across formats

        2. Ingredient Management
           - Ingredient normalization
           - Unit conversion
           - Nutritional calculation
           - Substitution handling
           Priority: High
           Dependencies: Core Recipe Processing
           Success Criteria: 98% ingredient match accuracy

        3. Stock Management
           - Pantry tracking
           - Stock level alerts
           - Usage prediction
           - Expiration tracking
           Priority: High
           Dependencies: Ingredient Management
           Success Criteria: 95% stock accuracy

    19.3 Optimization Features (P2)
        1. Performance Optimization
           - Caching implementation
           - Batch processing
           - Resource optimization
           - Response time improvement
           Priority: Medium
           Dependencies: Core Features
           Success Criteria: 50% performance improvement

        2. User Experience
           - Status notifications
           - Progress tracking
           - Error reporting
           - User feedback system
           Priority: Medium
           Dependencies: Core Features
           Success Criteria: 90% user satisfaction

        3. Automation
           - Scheduled processing
           - Automated updates
           - Workflow triggers
           - Integration automation
           Priority: Medium
           Dependencies: Enhanced Features
           Success Criteria: 80% reduction in manual tasks

    19.4 Future Enhancements (P3)
        1. AI/ML Integration
           - Recipe categorization
           - Ingredient prediction
           - Smart recommendations
           - Pattern learning
           Priority: Low
           Dependencies: Enhanced Features
           Success Criteria: 85% prediction accuracy

        2. Advanced Analytics
           - Usage analytics
           - Cost tracking
           - Nutrition analysis
           - Trend reporting
           Priority: Low
           Dependencies: Stock Management
           Success Criteria: Comprehensive reporting capability

        3. Extended Integration
           - Additional platforms
           - API extensions
           - Third-party services
           - Custom integrations
           Priority: Low
           Dependencies: Core Integration
           Success Criteria: 3+ new platform integrations

    19.5 Feature Dependencies
        ```mermaid
        graph TD
            A[Core Recipe Processing] --> B[Advanced Recipe Processing]
            A --> C[Notion Integration]
            B --> D[Ingredient Management]
            D --> E[Stock Management]
            C --> F[Automation]
            D --> G[AI/ML Integration]
            E --> H[Advanced Analytics]
            F --> I[Extended Integration]
        ```

    19.6 Implementation Timeline
        Phase 1 (Months 1-2)
        - Core Recipe Processing
        - Basic Notion Integration
        - Data Validation

        Phase 2 (Months 3-4)
        - Advanced Recipe Processing
        - Ingredient Management
        - Initial Stock Management

        Phase 3 (Months 5-6)
        - Performance Optimization
        - User Experience Improvements
        - Automation Implementation

        Phase 4 (Months 7-8)
        - AI/ML Features
        - Analytics
        - Extended Integrations

    19.7 Success Metrics
        - Feature Completion
          * Core Features: 100% completion
          * Enhanced Features: 90% completion
          * Optimization Features: 80% completion
          * Future Enhancements: 60% completion

        - Quality Metrics
          * Recipe Processing Accuracy: ≥ 95%
          * Data Consistency: 100%
          * System Uptime: ≥ 99.9%
          * User Satisfaction: ≥ 90%

        - Performance Metrics
          * Recipe Processing Time: < 5 seconds
          * Batch Processing: < 30 seconds for 10 recipes
          * API Response Time: < 1 second
          * Resource Utilization: < 70% peak

1. Overview

The Monthly Meal Plan is an automated recipe management and meal planning system that streamlines the process of digitizing, organizing, and planning meals. It transforms various recipe formats into a structured digital collection while managing pantry inventory and generating smart shopping lists.

    1.1 Core Functionality

    - Recipe Digitization: Processes recipes from multiple formats (PDF, JPG, TXT, Markdown)
    - Intelligent Parsing: Extracts and normalizes recipe components (ingredients, portions, instructions)
    - Nutritional Analysis: Calculates caloric content and tracks nutritional information
    - Inventory Management: Tracks pantry stock levels and generates shopping lists
    - Digital Organization: Maintains structured recipe collections in Notion

    1.2 System Components

    - Text Extraction Layer
    - OCR processing for images and PDFs
    - Text parsing and structure detection
    - Format-specific extractors

    - Recipe Processing Layer
    - Ingredient normalization and matching
    - Portion size standardization
    - Nutritional data calculation
    - Recipe metadata enrichment

    - Data Management Layer
    - Notion database integration
    - Recipe page creation and updates
    - Ingredient relationship management
    - Pantry stock tracking
    - Shopping list generation

    - Automation Layer
    - Workflow orchestration (via Pipedream/n8n)
    - Event logging and monitoring
    - Error handling and recovery
    - Automated testing and validation

    1.3 Key Features

    - Multi-format Support: Handles various recipe input formats seamlessly
    - Smart Parsing: Recognizes recipe components regardless of structure
    - Automated Organization: Creates and updates structured Notion pages
    - Inventory Tracking: Maintains real-time pantry stock levels
    - Shopping Automation: Generates lists based on meal plans and stock
    - Data Consistency: Ensures normalized ingredient data across recipes
    - Error Recovery: Robust handling of processing failures
    - Extensible Design: Modular architecture for easy feature additions

2. Goals

The Monthly Meal Plan project aims to create a robust, automated system for managing recipes and meal planning while ensuring data accuracy and user convenience.

    2.1 Primary Objectives

    - Recipe Management Excellence
    - Achieve 95%+ accuracy in recipe parsing and normalization
    - Support all common recipe formats (PDF, JPG, TXT, Markdown)
    - Maintain data consistency across recipe variations
    - Preserve original recipe formatting and styling when possible

    - Intelligent Data Processing
    - Implement smart ingredient recognition and matching
    - Standardize measurements and portion sizes automatically
    - Calculate accurate nutritional information
    - Handle recipe scaling with precision

    - Automation & Integration
    - Eliminate manual data entry and corrections
    - Maintain real-time synchronization with Notion
    - Prevent duplicate entries and data inconsistencies
    - Enable automated workflow triggers and notifications

    2.2 Technical Goals

    - Architecture & Performance
    - Achieve sub-5 second processing time per recipe
    - Maintain test coverage above 80%
    - Implement efficient caching strategies
    - Optimize memory usage for large recipe batches

    - Code Quality & Maintenance
    - Follow strict typing with mypy compliance
    - Maintain comprehensive documentation
    - Implement robust error handling and recovery
    - Establish clear logging and monitoring

    - Scalability & Extension
    - Design for multi-language support
    - Enable easy addition of new recipe sources
    - Support multiple Notion workspaces
    - Allow for future AI/ML enhancements

    2.3 Operational Goals

    - Data Management
    - Maintain accurate ingredient database
    - Update stock levels in real-time
    - Generate precise shopping lists
    - Track recipe usage and modifications

    - Error Handling
    - Achieve < 1% error rate in recipe processing
    - Implement automatic error recovery
    - Provide clear error reporting
    - Enable manual intervention points

    - Monitoring & Maintenance
    - Track system performance metrics
    - Monitor API rate limits and usage
    - Alert on critical failures
    - Maintain audit logs for all operations

    2.4 Success Metrics

    - Technical Metrics
    - Recipe Processing Accuracy: ≥ 95%
    - System Uptime: ≥ 99.9%
    - Average Processing Time: < 5 seconds/recipe
    - Test Coverage: ≥ 80%

    - Operational Metrics
    - Shopping List Accuracy: ≥ 95%
    - Stock Level Accuracy: ≥ 98%
    - Duplicate Detection Rate: ≥ 99%
    - Error Recovery Rate: ≥ 90%

    - Integration Metrics
    - Notion Sync Success Rate: ≥ 99%
    - API Rate Limit Compliance: 100%
    - Data Consistency Rate: ≥ 99.9%
    - Workflow Automation Success: ≥ 95%

    2.5 Database Integration Goals

    The system maintains four primary Notion databases with specific structures and relationships:

        2.5.1 Recetas (Recipes Database)

        Required Properties:
        - `Nombre` (Title): Main recipe title
        - `Calorías` (Number): Caloric content
        - `Porciones` (Number): Number of servings
        - `Tipo` (Select): Recipe type
        - `Tags` (Multi-select): Recipe categorization
        - `Hecho` (Checkbox): Completion status
        - `Relación con Ingredientes`: Relation to Ingredients database

        Content Structure:
        - Ingredients list as content blocks
        - Preparation steps
        - Calorie breakdown

        Objectives:
        - Maintain a single source of truth for all recipe information
        - Enable efficient recipe search and filtering
        - Support recipe versioning and modifications
        - Facilitate meal planning through clear categorization

        2.5.2 Alacena (Pantry Database)

        Required Properties:
        - `Name` (Title): Ingredient name
        - `Categoría` (Select): Ingredient category
        - `Unidad` (Select): Measurement unit (auto-populated)
        - `Stock alacena` (Number): Current stock level
        - `En lista de compras` (Checkbox): Shopping list status

        Planned Enhancements:
        - `Valor Nutricional` (Number): Nutritional value per standard unit
        - `Stock Mínimo` (Number): Calculated threshold for restock
        - `Alternativas` (Relation): Possible ingredient substitutes
        - `Último Precio` (Number): Cost tracking
        - `Marca Preferida` (Text): Quality control reference
        - `Notas de Almacenamiento` (Text): Storage handling instructions
        - `Última Actualización` (Date): Stock check timestamp
        - `Fecha de Caducidad` (Date): Expiry tracking
        - `Fecha de Compra` (Date): Purchase date for rotation

        Objectives:
        - Maintain accurate real-time stock levels
        - Trigger timely restock notifications
        - Track ingredient usage patterns
        - Support inventory audits

        2.5.3 Ingredientes (Recipe Ingredients Database)

        Required Properties:
        - `Cantidad Usada` (Title): Amount used
        - `Unidad` (Text): Unit of measurement
        - `Relación con Receta`: Relation to recipe
        - `Relación con Ingrediente`: Relation to pantry ingredient

        Objectives:
        - Track ingredient usage across recipes
        - Maintain consistent measurements
        - Enable ingredient substitutions
        - Support recipe scaling

        2.5.4 Lista de Compras (Shopping List Database)

        Required Properties:
        - `Producto` (Title): Item to purchase
        - `Cantidad` (Number): Amount needed
        - `Categoría` (Select): Shopping category
        - `Comprado` (Checkbox): Purchase status

        Planned Enhancements:
        - `Prioridad` (Select): Purchase urgency level
        - `Relación con Ingrediente` (Relation): Direct link to pantry ingredient
        - `Fecha Objetivo` (Date): Target purchase date
        - `Notas de Compra` (Text): Special purchase instructions

        Objectives:
        - Generate accurate shopping requirements
        - Optimize shopping efficiency
        - Track purchase completion
        - Support multiple shopping locations

        Integration Requirements:
        - Real-time synchronization between databases
        - Automatic property updates on related records
        - Validation of relational integrity
        - History tracking of all modifications
        - Error handling for failed updates
        - Rate limit compliance for API calls

        Database Relationships:
        1. Recipes → Ingredients (one-to-many)
        - Each recipe contains multiple ingredients
        - Ingredients track their usage in recipes

        2. Pantry → Shopping List (one-to-one)
        - Low stock items trigger shopping list entries
        - Purchase updates stock levels

        3. Ingredients → Pantry (many-to-one)
        - Recipe ingredients link to pantry items
        - Stock levels affect recipe availability

3. Context & Scope

Input Scope:
- Supported file formats: PDF, JPG (multi-page), TXT, Markdown
- Recipe complexity: Simple to complex multi-step recipes
- Language support: English and Spanish from initial release
  - Dual language ingredient database
  - Language-specific measurement conventions
  - Regional recipe variations support
  - Automatic language detection
- Image requirements: Minimum 300 DPI for OCR

Output Scope:
- Notion database updates
  - Bilingual recipe titles and descriptions
  - Language-specific ingredient names
  - Unit conversions based on regional preferences
- Automated notifications in user's preferred language
- Error reports and logs (system logs in English, user messages bilingual)
- Performance metrics

System Boundaries:
- Backend processing only
- No user interface
- API-driven integration
- Automated workflow triggers
- Language-specific data validation rules

Additional Language Considerations:
- Ingredient name normalization across languages
- Regional measurement system preferences (metric/imperial)
- Culture-specific recipe categorization
- Language-specific recipe formatting conventions
- Cross-language recipe search capabilities

4. Page Structure & Views

    4.1 Recipe Pages

        Design Philosophy:
        - Recipes are full-page documents, not property-based entries
        - Content is presented in a readable, cooking-friendly format
        - Content is displayed in its original language (English or Spanish)
        - Properties are used for organization but not primary display
        - Consistent visual hierarchy across all recipes

        Page Structure:
        1. Header Section
        - Recipe title (in Spanish)
        - Hero image
        - Quick overview:
            * "Porciones" (portions)
            * "Tiempo de preparación" (prep time)
            * "Dificultad" (difficulty)
        - Source attribution

        2. Main Content
        - "Ingredientes" section as content blocks
        - "Preparación" with step-by-step instructions
        - "Notas y consejos" (notes and tips)
        - Time breakdown:
            * "Preparación" (prep)
            * "Cocción" (cooking)
            * "Total"
        - "Conservación y servido" (storage and serving)

        3. Metadata (Hidden Properties)
        - Technical properties for database relations
        - Tags and categories using Spanish conventions
        - Nutritional information
        - Version tracking
        - Last updated timestamp

    4.2 Database Views

        1. Recipe Collection View
        - Gallery view with recipe images
        - List view for quick scanning
        - Table view for bulk operations
        - Filtered views by:
            * "Tipo de comida" (meal type)
            * "Tipo de cocina" (cuisine)
            * "Tiempo de preparación" (prep time)
            * "Última vez cocinada" (last cooked)
            * "Favoritas" (favorites)

        2. Calendar View
        - Monthly meal planning
        - Visual meal type distribution
        - Portion planning
        - Shopping list generation triggers
        - Color coding by cuisine type

        3. Ingredient Database View
        - Table view for inventory management
        - Gallery view for visual reference
        - Filtered views by:
            * "Categoría" (category)
            * "Estado de stock" (stock status)
            * "Urgencia de compra" (shopping urgency)
            * "Control de caducidad" (expiration tracking)

        4. Shopping List View
        - Kanban view by status
        - List view grouped by store sections ("Secciones")
        - Mobile-optimized view for in-store use
        - Purchase tracking

    4.3 View-Specific Features

        Recipe Full Page:
        - Rich text formatting for instructions
        - Checkbox lists for ingredients
        - Collapsible sections for variations
        - Image galleries for step-by-step photos
        - Print-friendly layout
        - Mobile-optimized reading view

        Calendar View:
        - Drag-and-drop meal planning
        - Automatic portion calculation
        - Shopping list generation
        - Meal distribution visualization

        Collection Views:
        - Custom sorting options
        - Quick filters for dietary restrictions ("Restricciones alimentarias")
        - Bulk operations for meal planning
        - Search optimization for Spanish terms
        - Template buttons for new entries

    4.4 Integration Points

        Automated Updates:
        - Recipe imports maintain Spanish formatting
        - Property updates preserve page layout
        - Image processing and placement
        - Version history preservation

        User Experience:
        - Consistent navigation between views
        - Quick access to frequently used filters
        - Mobile-friendly interaction
        - Print-optimized recipe pages
        - Cross-linking between related recipes
        - Search optimized for Spanish terms and synonyms

5. Development Setup

    5.1 Environment Setup

    1. System Requirements
       ```bash
       # Required system packages
       sudo apt-get update && sudo apt-get install -y \
           python3.13 \
           python3.13-venv \
           tesseract-ocr \
           poppler-utils \
           git \
           build-essential

       # Verify installations
       python3.13 --version
       tesseract --version
       pdftoppm -v
       ```

    2. Python Virtual Environment
       ```bash
       # Create virtual environment
       python3.13 -m venv .venv

       # Activate virtual environment
       source .venv/bin/activate

       # Upgrade pip
       pip install --upgrade pip
       ```

    3. Project Structure Setup
       ```bash
       mkdir -p core/{extraction,recipe,notion,storage,utils}
       mkdir -p tests/{unit,integration,migration}/
       mkdir -p tests/fixtures/{recipes,notion}
       touch README.md
       ```

    5.2 Dependencies

    1. Core Dependencies
       ```toml
       # requirements.txt
       # Core functionality
       notion-client==2.3.0
       pdf2image==1.17.0
       pytesseract==0.3.13
       pdfplumber==0.11.6
       pillow==11.2.1

       # Async support
       httpx==0.28.1
       anyio==4.9.0

       # Utilities
       python-dotenv==1.1.0
       pydantic==2.6.3
       structlog==24.1.0

       # Type checking
       mypy==1.15.0
       types-all==1.0.0
       ```

    2. Development Dependencies
       ```toml
       # requirements-dev.txt
       # Testing
       pytest==8.3.5
       pytest-asyncio==0.23.5
       pytest-cov==6.1.1
       pytest-benchmark==4.0.0
       hypothesis==6.98.8

       # Linting and formatting
       black==24.2.0
       isort==5.13.2
       flake8==7.0.0
       flake8-docstrings==1.7.0
       pylint==3.1.0

       # Type checking
       mypy==1.15.0
       types-all==1.0.0

       # Development tools
       pre-commit==4.2.0
       ```

    3. Installation
       ```bash
       # Install production dependencies
       pip install -r requirements.txt

       # Install development dependencies
       pip install -r requirements-dev.txt

       # Install pre-commit hooks
       pre-commit install
       ```

    5.3 Configuration

    1. Environment Variables
       ```bash
       # .env
       # Notion API Configuration
       NOTION_TOKEN=your_integration_token
       NOTION_RECIPE_DB=your_recipe_database_id
       NOTION_INGREDIENTS_DB=your_ingredients_database_id
       NOTION_PANTRY_DB=your_pantry_database_id
       NOTION_SHOPPING_LIST_DB=your_shopping_list_database_id

       # Application Settings
       LOG_LEVEL=INFO
       ENVIRONMENT=development
       ENABLE_PERFORMANCE_LOGGING=true
       CACHE_ENABLED=true

       # OCR Configuration
       TESSERACT_PATH=/usr/bin/tesseract
       OCR_LANGUAGE=spa+eng
       ```

    2. Configuration Management
       ```python
       # core/utils/config.py
       from pathlib import Path
       from typing import Dict, Any
       from pydantic import BaseSettings

       class Settings(BaseSettings):
           # Notion Configuration
           notion_token: str
           notion_recipe_db: str
           notion_ingredients_db: str
           notion_pantry_db: str
           notion_shopping_list_db: str

           # Application Settings
           log_level: str = "INFO"
           environment: str = "development"
           enable_performance_logging: bool = True
           cache_enabled: bool = True

           # OCR Configuration
           tesseract_path: Path = Path("/usr/bin/tesseract")
           ocr_language: str = "spa+eng"

           class Config:
               env_file = ".env"
               env_file_encoding = "utf-8"

       settings = Settings()
       ```

    3. Logging Configuration
       ```python
       # core/utils/logger.py
       import structlog
       from typing import Any, Dict

       def setup_logging() -> None:
           """Configure structured logging."""
           structlog.configure(
               processors=[
                   structlog.contextvars.merge_contextvars,
                   structlog.processors.add_log_level,
                   structlog.processors.TimeStamper(fmt="iso"),
                   structlog.processors.StackInfoRenderer(),
                   structlog.processors.format_exc_info,
                   structlog.processors.UnicodeDecoder(),
                   structlog.processors.JSONRenderer()
               ],
               logger_factory=structlog.PrintLoggerFactory(),
               wrapper_class=structlog.make_filtering_bound_logger(
                   settings.log_level
               ),
               cache_logger_on_first_use=True
           )

       logger = structlog.get_logger()
       ```

    5.4 Security & Permissions

    1. API Token Management
       ```python
       # core/utils/security.py
       from datetime import datetime, timedelta
       from typing import Optional
       import os
       import json

       class TokenManager:
           def __init__(self):
               self.token_file = Path(".tokens")
               self.token_data = self._load_tokens()

           def _load_tokens(self) -> Dict[str, Any]:
               if self.token_file.exists():
                   return json.loads(self.token_file.read_text())
               return {}

           def rotate_token(self, service: str, new_token: str) -> None:
               """Rotate API token with audit logging."""
               old_token = self.token_data.get(service, {}).get("token")
               self.token_data[service] = {
                   "token": new_token,
                   "created_at": datetime.now().isoformat(),
                   "previous_token": old_token
               }
               self._save_tokens()
               logger.info("Token rotated", service=service)

           def get_token(self, service: str) -> Optional[str]:
               """Get current token with expiration check."""
               token_info = self.token_data.get(service, {})
               if not token_info:
                   return None

               created_at = datetime.fromisoformat(token_info["created_at"])
               if datetime.now() - created_at > timedelta(days=89):
                   logger.warning("Token near expiration", service=service)

               return token_info["token"]
       ```

    2. File Permissions
       ```python
       # core/utils/security.py
       def secure_file_permissions() -> None:
           """Set secure permissions for sensitive files."""
           sensitive_files = [
               ".env",
               ".tokens",
               "credentials.json"
           ]

           for file in sensitive_files:
               path = Path(file)
               if path.exists():
                   # Set to user read/write only (600)
                   path.chmod(0o600)
                   logger.info("Secured file permissions", file=file)
       ```

    3. Input Validation
       ```python
       # core/utils/validation.py
       from typing import Any, Dict
       import re
       from pydantic import BaseModel, validator

       class RecipeInput(BaseModel):
           title: str
           ingredients: List[Dict[str, Any]]
           instructions: List[str]

           @validator("title")
           def sanitize_title(cls, v: str) -> str:
               """Sanitize recipe title input."""
               # Remove potential XSS/injection patterns
               v = re.sub(r"[<>\"'%;)(&+]", "", v)
               return v.strip()

           @validator("ingredients")
           def validate_ingredients(cls, v: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
               """Validate ingredient entries."""
               required_fields = {"name", "quantity", "unit"}
               for ingredient in v:
                   if not all(field in ingredient for field in required_fields):
                       raise ValueError("Missing required ingredient fields")
               return v
       ```

    5.5 Development Tools

    1. Pre-commit Configuration
       ```yaml
       # .pre-commit-config.yaml
       repos:
         - repo: https://github.com/pre-commit/pre-commit-hooks
           rev: v4.5.0
           hooks:
             - id: trailing-whitespace
             - id: end-of-file-fixer
             - id: check-yaml
             - id: check-json
             - id: check-added-large-files
             - id: debug-statements
             - id: requirements-txt-fixer

         - repo: https://github.com/psf/black
           rev: 24.3.0
           hooks:
             - id: black
               args: [--line-length=88]

         - repo: https://github.com/PyCQA/isort
           rev: 5.13.2
           hooks:
             - id: isort
               args: ["--profile", "black", "--filter-files"]

         - repo: https://github.com/pre-commit/mirrors-mypy
           rev: v1.9.0
           hooks:
             - id: mypy
               args: [--ignore-missing-imports]

         - repo: https://github.com/PyCQA/flake8
           rev: 7.0.0
           hooks:
             - id: flake8
               args: [--max-line-length=88]
               additional_dependencies:
                 - flake8-docstrings
                 - flake8-bugbear
                 - flake8-comprehensions

         - repo: https://github.com/commitizen-tools/commitizen
           rev: v3.20.0
           hooks:
             - id: commitizen
               stages: [commit-msg]
       ```

    2. VS Code Configuration
       ```json
       // .vscode/settings.json
       {
           "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
           "python.linting.enabled": true,
           "python.linting.pylintEnabled": true,
           "python.linting.flake8Enabled": true,
           "python.formatting.provider": "black",
           "editor.formatOnSave": true,
           "editor.codeActionsOnSave": {
               "source.organizeImports": true
           },
           "python.testing.pytestEnabled": true,
           "python.testing.unittestEnabled": false,
           "python.testing.nosetestsEnabled": false,
           "python.testing.pytestArgs": [
               "tests"
           ]
       }
       ```

    5.6 Quick Start Guide

    1. Initial Setup
       ```bash
       # Clone repository
       git clone https://github.com/yourusername/plan-mensual-comidas.git
       cd plan-mensual-comidas

       # Create and activate virtual environment
       python3.13 -m venv .venv
       source .venv/bin/activate

       # Install dependencies
       pip install -r requirements.txt
       pip install -r requirements-dev.txt

       # Set up pre-commit hooks
       pre-commit install

       # Copy and configure environment variables
       cp .env.example .env
       # Edit .env with your values
       ```

    2. Development Workflow
       ```bash
       # Create a new feature branch
       git checkout -b feature/new-feature

       # Run tests
       pytest

       # Run type checking
       mypy core tests

       # Format code
       black .
       isort .

       # Run linting
       flake8

       # Commit changes (pre-commit hooks will run automatically)
       git add .
       git commit -m "feat: add new feature"
       ```

    3. Common Development Tasks
       ```bash
       # Run specific test category
       pytest tests/unit
       pytest tests/integration
       pytest tests/migration

       # Run with coverage report
       pytest --cov=core --cov-report=html

       # Run performance benchmarks
       pytest tests/performance --benchmark-only

       # Generate documentation
       pdoc --html core/

       # Clean up cache files
       find . -type d -name "__pycache__" -exec rm -r {} +
       find . -type d -name ".pytest_cache" -exec rm -r {} +
       find . -type d -name ".mypy_cache" -exec rm -r {} +
       ```

6. Core Components

   - Text Extraction Layer

        ```python
        core/extraction/
        ├── __init__.py
        ├── interface.py     # Common extraction interface
        ├── pdf.py          # PDF extraction implementation
        ├── ocr.py          # OCR processing implementation
        └── text.py         # Plain text extraction implementation

        # Example Interface
        class IExtractor(ABC):
            @abstractmethod
            def extract(self, source_path: str) -> str:
                """Extract raw text from the given source file."""
                pass

            @abstractmethod
            def validate(self, source_path: str) -> bool:
                """Validate if file can be processed."""
                pass
        ```

   - Recipe Processing Layer

        ```python
        core/recipe/
        ├── __init__.py
        ├── models/
        │   ├── recipe.py          # Recipe data model
        │   ├── ingredient.py      # Ingredient data model
        │   └── metadata.py        # Metadata model
        ├── extractors/
        │   ├── base.py           # Base extractor interface
        │   ├── sections.py       # Section extraction
        │   ├── ingredients.py    # Ingredient extraction
        │   └── metadata.py       # Metadata extraction
        ├── normalizers/
        │   ├── base.py          # Base normalizer interface
        │   ├── ingredients.py   # Ingredient normalization
        │   ├── measurements.py  # Measurement standardization
        │   └── text.py         # Text normalization
        └── processor.py        # Main recipe processor

        # Example Recipe Model
        @dataclass
        class Recipe:
            title: str
            ingredients: List[Ingredient]
            instructions: List[str]
            metadata: RecipeMetadata
            source: Optional[str] = None
            created_at: datetime = field(default_factory=datetime.now)
            updated_at: datetime = field(default_factory=datetime.now)
        ```

   - Notion Integration Layer

        ```python
        core/notion/
        ├── __init__.py
        ├── client.py       # Notion API client
        ├── sync.py         # Database synchronization
        ├── models.py       # Notion data models
        └── errors.py       # Error handling

        # Example Client Usage
        class NotionClient:
            def __init__(self):
                self._setup_rate_limiting()
                self._init_error_handling()

            async def create_recipe(self, recipe: Recipe) -> str:
                """Create a new recipe page in Notion.

                Args:
                    recipe: Recipe object containing normalized data

                Returns:
                    str: Notion page ID of created recipe

                Raises:
                    NotionAPIError: If creation fails
                """
                properties = self._map_recipe_to_properties(recipe)
                return await self._make_api_call(
                    "pages.create",
                    parent={"database_id": self.recipe_db_id},
                    properties=properties
                )

            @retry(max_attempts=3, backoff=exponential_backoff)
            async def _make_api_call(self, method: str, **kwargs):
                """Make rate-limited API call with retries."""
                return await self._client.make_request(method, **kwargs)
        ```

   - Storage Layer

        ```python
        core/storage/
        ├── __init__.py
        ├── manager.py      # Storage operations
        └── models.py       # Storage models

        # Example Storage Manager
        class StorageManager:
            def __init__(self):
                self.recipe_dir = Path("recipes")
                self.processed_dir = Path("processed")
                self.failed_dir = Path("failed")

            async def store_recipe(self, recipe: Recipe, content: str):
                """Store recipe and its original content."""
                recipe_path = self.recipe_dir / f"{recipe.id}.json"
                content_path = self.recipe_dir / f"{recipe.id}.txt"

                await self._atomic_write(recipe_path, recipe.to_json())
                await self._atomic_write(content_path, content)
        ```

   - Utils Layer

        ```python
        core/utils/
        ├── __init__.py
        ├── config.py       # Configuration management
        ├── logger.py       # Logging system
        ├── metrics.py      # Performance metrics
        └── errors.py       # Error handling

        # Example Configuration
        class Config:
            def __init__(self):
                self.settings = self._load_settings()
                self._setup_logging()
                self._init_metrics()

       def _load_settings(self) -> Dict[str, Any]:
           """Load configuration from environment and files."""
           return {
               "notion_token": os.getenv("NOTION_TOKEN"),
               "recipe_db_id": os.getenv("NOTION_RECIPE_DB"),
               "log_level": os.getenv("LOG_LEVEL", "INFO"),
               "metrics_enabled": os.getenv("METRICS_ENABLED", "true").lower() == "true"
           }
   ```

7. Operations
   - Monitoring & Metrics
   - Logging Strategy
   - Error Handling
   - Performance Considerations

8. Testing Strategy

    8.1 Test Categories

    1. Unit Tests (By Module)
       - Extraction Layer Tests:
         ```python
         @pytest.mark.unit
         class TestPDFExtractor:
             def test_extract_text_from_pdf(self):
                 extractor = PDFExtractor()
                 text = extractor.extract("test.pdf")
                 assert "Ingredients:" in text
                 assert "Instructions:" in text
         ```

       - Recipe Processing Tests:
         ```python
         @pytest.mark.unit
         class TestIngredientParser:
             def test_parse_ingredient_line(self):
                 parser = IngredientParser()
                 result = parser.parse("2 cups flour")
                 assert result.quantity == 2
                 assert result.unit == "cups"
                 assert result.name == "flour"
         ```

       - Notion Integration Tests:
         ```python
         @pytest.mark.unit
         class TestNotionClient:
             async def test_create_recipe_page(self):
                 client = NotionClient()
                 recipe = Recipe(title="Test Recipe")
                 page_id = await client.create_recipe(recipe)
                 assert page_id is not None
         ```

    2. Integration Tests (Workflow-Based)
       ```python
       @pytest.mark.integration
       class TestRecipeWorkflow:
           async def test_pdf_to_notion_workflow(self):
               # Test complete workflow from PDF to Notion
               pdf_path = "tests/fixtures/recipes/sample.pdf"

               # 1. Extract text
               extractor = PDFExtractor()
               text = extractor.extract(pdf_path)

               # 2. Process recipe
               processor = RecipeProcessor()
               recipe = processor.process(text)

               # 3. Upload to Notion
               notion = NotionClient()
               result = await notion.create_recipe(recipe)

               assert result.success
               assert result.page_id is not None
       ```

    8.2 Test Data Management

    1. Migration Test Data
       ```python
       @pytest.fixture(scope="session")
       def migration_test_data():
           """Provide test data for migration validation"""
           return {
               "recipes": [
                   {
                       "old_format": "tests/fixtures/legacy/recipe1.txt",
                       "new_format": "tests/fixtures/current/recipe1.txt",
                       "expected_result": "tests/fixtures/expected/recipe1.json"
                   }
               ]
           }
       ```

    2. Module-Specific Fixtures
       ```python
       # tests/conftest.py
       @pytest.fixture(scope="module")
       def pdf_extractor():
           return PDFExtractor()

       @pytest.fixture(scope="module")
       def recipe_processor():
           return RecipeProcessor()

       @pytest.fixture(scope="module")
       def notion_client():
           return NotionClient(token=os.getenv("TEST_NOTION_TOKEN"))
       ```

    8.3 Performance Testing

    1. Module-Level Benchmarks
       ```python
       @pytest.mark.benchmark
       class TestExtractionPerformance:
           def test_pdf_extraction_performance(self, benchmark):
               extractor = PDFExtractor()
               result = benchmark(extractor.extract, "large_recipe.pdf")
               assert result.stats.mean < 5.0  # Under 5 seconds

       @pytest.mark.benchmark
       class TestRecipeProcessingPerformance:
           def test_recipe_processing_performance(self, benchmark):
               processor = RecipeProcessor()
               result = benchmark(processor.process, "complex_recipe.txt")
               assert result.stats.mean < 2.0  # Under 2 seconds
       ```

    2. Migration Performance Comparison
       ```python
       @pytest.mark.benchmark
       class TestMigrationPerformance:
           def test_extraction_performance_comparison(self, benchmark_group):
               old = benchmark_group.pedantic(
                   legacy_extract_pdf,
                   args=["test.pdf"],
                   iterations=100
               )
               new = benchmark_group.pedantic(
                   new_extract_pdf,
                   args=["test.pdf"],
                   iterations=100
               )
               # New version should be at least as fast
               assert new.stats.mean <= old.stats.mean * 1.1
       ```

    8.4 Continuous Integration

    ```yaml
    # .github/workflows/test.yml
    name: Test Suite
    on: [push, pull_request]

    jobs:
      test:
        runs-on: ubuntu-latest
        strategy:
          matrix:
            python-version: ['3.13']
            test-type: ['unit', 'integration', 'migration']

        steps:
          - uses: actions/checkout@v2
          - name: Set up Python
            uses: actions/setup-python@v2
            with:
              python-version: ${{ matrix.python-version }}

          - name: Install dependencies
            run: |
              python -m pip install --upgrade pip
              pip install -r requirements.txt
              pip install -r requirements-test.txt

          - name: Run tests
            run: |
              if [ "${{ matrix.test-type }}" = "unit" ]; then
                pytest tests/unit/
              elif [ "${{ matrix.test-type }}" = "integration" ]; then
                pytest tests/integration/
              else
                pytest tests/migration/
              fi
    ```

    8.5 Test Documentation

    1. Test Plan Template
       ```markdown
       # Test Plan: [Module Name]

       ## Scope
       - Components being tested
       - Migration phase coverage
       - Test categories included

       ## Test Cases
       1. Unit Tests
          - [ ] Component functionality
          - [ ] Error handling
          - [ ] Edge cases

       2. Integration Tests
          - [ ] Workflow validation
          - [ ] Component interaction
          - [ ] Migration compatibility

       3. Performance Tests
          - [ ] Benchmark metrics
          - [ ] Resource usage
          - [ ] Comparison with legacy system

       ## Success Criteria
       - All tests passing
       - Performance within benchmarks
       - Migration validation complete
       ```

9. Development Process
   - Code Conventions
   - Git Workflow
   - CI/CD Pipeline
   - Release Process

10. Version Roadmap

11. System Architecture

    11.1 Component Overview

    The system is built around five main layers:

    1. Text Extraction Layer
       - Handles multiple input formats (PDF, Image, Text)
       - Provides unified extraction interface
       - Manages OCR and text processing
       - Validates input formats

    2. Recipe Processing Layer
       - Processes extracted text into structured data
       - Normalizes ingredients and measurements
       - Extracts recipe metadata
       - Validates recipe structure

    3. Notion Integration Layer
       - Manages Notion API communication
       - Handles rate limiting and retries
       - Synchronizes database updates
       - Manages error recovery

    4. Storage Layer
       - Manages local file operations
       - Handles atomic writes
       - Organizes processed files
       - Maintains backup copies

    5. Utils Layer
       - Provides configuration management
       - Handles logging and monitoring
       - Manages error handling
       - Collects performance metrics

    11.2 Data Flow

    1. Input Processing:
       ```mermaid
       graph TD
           A[Input File] --> B[Text Extraction]
           B --> C[Content Validation]
           C --> D[Text Normalization]
           D --> E[Recipe Processing]
       ```

    2. Recipe Processing:
       ```mermaid
       graph TD
           A[Raw Text] --> B[Section Extraction]
           B --> C[Ingredient Parsing]
           B --> D[Instruction Parsing]
           B --> E[Metadata Extraction]
           C --> F[Ingredient Normalization]
           D --> G[Instruction Normalization]
           E --> H[Metadata Validation]
           F --> I[Recipe Assembly]
           G --> I
           H --> I
       ```

    3. Notion Integration:
       ```mermaid
       graph TD
           A[Recipe Object] --> B[Property Mapping]
           B --> C[Rate Limiting]
           C --> D[API Request]
           D --> E[Error Handling]
           E --> F[Retry Logic]
           F --> G[Success/Failure]
       ```

    11.3 Error Handling

    1. Extraction Errors:
       - Invalid file formats
         * Unsupported file types
         * Corrupted file structures
         * Invalid encodings
         * Recovery: Attempt format detection and conversion
         * Fallback: Move to error directory with detailed report

       - OCR failures
         * Low image quality
         * Unrecognizable text
         * Language detection issues
         * Recovery: Retry with different OCR settings
         * Fallback: Flag for manual review

       - Encoding issues
         * Non-UTF8 encodings
         * Special character corruption
         * Binary file detection
         * Recovery: Auto-detect and convert encodings
         * Fallback: Request manual file review

       - Corrupted files
         * Incomplete downloads
         * Partial content
         * File system errors
         * Recovery: Verify file integrity
         * Fallback: Request file re-upload

    2. Processing Errors:
       - Invalid recipe structure
         * Missing sections
         * Malformed content
         * Unexpected formatting
         * Recovery: Apply structure inference
         * Fallback: Template-based reconstruction

       - Missing required data
         * Incomplete ingredients
         * Missing quantities
         * Undefined units
         * Recovery: Apply default values where safe
         * Fallback: Queue for manual completion

       - Normalization failures
         * Unknown ingredients
         * Non-standard measurements
         * Ambiguous instructions
         * Recovery: Use fuzzy matching
         * Fallback: Add to normalization database

       - Validation errors
         * Schema violations
         * Data type mismatches
         * Range violations
         * Recovery: Auto-correct when confidence is high
         * Fallback: Log validation issues

    3. Integration Errors:
       - API rate limits
         * Notion API throttling
         * Concurrent request limits
         * Recovery: Implement exponential backoff
         * Strategy: Token bucket rate limiting
         ```python
         class RateLimiter:
             def __init__(self, rate_limit: int, time_window: int):
                 self.rate_limit = rate_limit
                 self.time_window = time_window
                 self.tokens = rate_limit
                 self.last_update = time.time()

             async def acquire(self):
                 now = time.time()
                 time_passed = now - self.last_update
                 self.tokens = min(
                     self.rate_limit,
                     self.tokens + time_passed * (self.rate_limit / self.time_window)
                 )

                 if self.tokens < 1:
                     wait_time = (1 - self.tokens) * (self.time_window / self.rate_limit)
                     await asyncio.sleep(wait_time)
                     return await self.acquire()

                 self.tokens -= 1
                 self.last_update = now
                 return True
         ```

       - Network failures
         * Connection timeouts
         * DNS resolution errors
         * SSL/TLS issues
         * Recovery: Circuit breaker pattern
         ```python
         class CircuitBreaker:
             def __init__(self, failure_threshold: int, reset_timeout: int):
                 self.failure_threshold = failure_threshold
                 self.reset_timeout = reset_timeout
                 self.failures = 0
                 self.last_failure = 0
                 self.state = "closed"  # closed, open, half-open

             async def call(self, func, *args, **kwargs):
                 if self.state == "open":
                     if time.time() - self.last_failure > self.reset_timeout:
                         self.state = "half-open"
                     else:
                         raise CircuitBreakerError("Circuit is open")

                 try:
                     result = await func(*args, **kwargs)
                     if self.state == "half-open":
                         self.state = "closed"
                         self.failures = 0
                     return result
                 except Exception as e:
                     self.failures += 1
                     self.last_failure = time.time()
                     if self.failures >= self.failure_threshold:
                         self.state = "open"
                     raise
         ```

       - Authentication issues
         * Invalid tokens
         * Token expiration
         * Permission changes
         * Recovery: Token refresh and rotation
         ```python
         class TokenManager:
             def __init__(self, initial_token: str, refresh_interval: int = 86400):
                 self.current_token = initial_token
                 self.refresh_interval = refresh_interval
                 self.last_refresh = time.time()

             async def get_valid_token(self):
                 if time.time() - self.last_refresh > self.refresh_interval:
                     await self.refresh_token()
                 return self.current_token

             async def refresh_token(self):
                 try:
                     new_token = await self._request_new_token()
                     self.current_token = new_token
                     self.last_refresh = time.time()
                 except Exception as e:
                     logger.error(f"Token refresh failed: {e}")
                     raise
         ```

       - Data validation errors
         * Schema mismatches
         * Required field violations
         * Type conversion errors
         * Recovery: Data normalization pipeline
         ```python
         class DataValidator:
             def __init__(self):
                 self.normalizers = {
                     "ingredients": self._normalize_ingredients,
                     "portions": self._normalize_portions,
                     "instructions": self._normalize_instructions
                 }

             async def validate_and_normalize(self, data: Dict[str, Any]) -> Dict[str, Any]:
                 normalized = {}
                 errors = []

                 for field, value in data.items():
                     try:
                         if field in self.normalizers:
                             normalized[field] = await self.normalizers[field](value)
                         else:
                             normalized[field] = value
                     except ValidationError as e:
                         errors.append(f"{field}: {str(e)}")

                 if errors:
                     raise ValidationError("\n".join(errors))
                 return normalized
         ```

    4. Error Recovery Strategy:
       - Immediate Recovery
         * Retry with exponential backoff
         * Alternative processing paths
         * Fallback to defaults
         * Automatic correction attempts

       - Delayed Recovery
         * Queue for background processing
         * Scheduled retry attempts
         * Manual intervention requests
         * Batch processing of similar errors

       - Monitoring & Alerting
         * Error rate tracking
         * Pattern detection
         * Severity classification
         * Alert routing based on type

       - Documentation & Reporting
         * Detailed error logs
         * Recovery attempt history
         * Resolution steps taken
         * Impact assessment

    5. Error Prevention:
       - Input Validation
         * File format verification
         * Content structure checking
         * Data type validation
         * Range and constraint checking

       - Proactive Monitoring
         * System health checks
         * Resource utilization tracking
         * API quota monitoring
         * Performance metrics

       - Automated Testing
         * Unit tests for error cases
         * Integration test scenarios
         * Chaos testing
         * Recovery procedure validation

    11.4 Performance Considerations

    1. Resource Management:
       - Memory usage monitoring
       - CPU utilization tracking
       - Disk space management
       - Network bandwidth control

    2. Optimization Strategies:
       - Batch processing for multiple recipes
       - Caching of common operations
       - Asynchronous API calls
       - Parallel text processing

    3. Monitoring:
       - Performance metrics collection
       - Error rate tracking
       - Resource usage monitoring
       - API quota management

    11.5 System Flow Diagrams

    1. Overall System Architecture:
    ```mermaid
    graph TD
        subgraph Input
            A[Recipe File] --> B[File Detection]
            B --> C[Text Extraction Layer]
        end

        subgraph Processing
            C --> D[Recipe Processing Layer]
            D --> E[Data Validation]
            E --> F[Recipe Assembly]
        end

        subgraph Integration
            F --> G[Notion Integration Layer]
            G --> H[Database Updates]
            H --> I[Sync Validation]
        end

        subgraph Storage
            F --> J[Local Storage]
            J --> K[Backup Management]
        end

        subgraph Monitoring
            L[Metrics Collection]
            M[Error Tracking]
            N[Performance Monitoring]
        end

        B -- Error --> M
        D -- Error --> M
        G -- Error --> M
        J -- Error --> M
    ```

    2. Recipe Processing Pipeline:
    ```mermaid
    graph TD
        subgraph Text_Extraction
            A[Input File] --> B[Format Detection]
            B --> C[OCR/Text Extraction]
            C --> D[Text Normalization]
        end

        subgraph Content_Processing
            D --> E[Section Detection]
            E --> F[Ingredient List]
            E --> G[Instructions]
            E --> H[Metadata]

            F --> I[Ingredient Parser]
            I --> J[Measurement Normalization]
            J --> K[Ingredient Validation]

            G --> L[Step Parser]
            L --> M[Step Validation]

            H --> N[Metadata Parser]
            N --> O[Metadata Validation]
        end

        subgraph Recipe_Assembly
            K --> P[Recipe Object]
            M --> P
            O --> P
            P --> Q[Validation]
            Q --> R[Final Recipe]
        end
    ```

    3. Notion Integration Flow:
    ```mermaid
    graph TD
        subgraph Recipe_Preparation
            A[Recipe Object] --> B[Property Mapping]
            B --> C[Data Validation]
        end

        subgraph API_Integration
            C --> D[Rate Limit Check]
            D --> E[Token Validation]
            E --> F[API Request]

            F -- Success --> G[Response Processing]
            F -- Error --> H[Error Handler]

            H -- Retry --> D
            H -- Fatal --> I[Error Notification]

            G --> J[Response Validation]
            J -- Invalid --> H
            J -- Valid --> K[Update Complete]
        end

        subgraph Synchronization
            K --> L[Local State Update]
            L --> M[Backup Creation]
            M --> N[Cleanup]
        end
    ```

    4. Error Handling Flow:
    ```mermaid
    graph TD
        subgraph Error_Detection
            A[Error Occurs] --> B{Error Type}
            B -- Validation --> C[Validation Handler]
            B -- Network --> D[Network Handler]
            B -- System --> E[System Handler]
        end

        subgraph Error_Processing
            C --> F{Severity Check}
            D --> F
            E --> F

            F -- Critical --> G[Emergency Response]
            F -- Warning --> H[Recovery Attempt]
            F -- Info --> I[Log & Continue]
        end

        subgraph Recovery
            G --> J[System Halt]
            G --> K[Admin Alert]

            H --> L[Retry Logic]
            L -- Success --> M[Resume Operation]
            L -- Failure --> N[Fallback Action]

            I --> O[Metrics Update]
            O --> P[Continue Processing]
        end
    ```

    5. Data Synchronization Flow:
    ```mermaid
    graph TD
        subgraph Local_Changes
            A[Recipe Update] --> B[Change Detection]
            B --> C[Change Queue]
        end

        subgraph Sync_Process
            C --> D[Batch Collection]
            D --> E[Priority Sorting]
            E --> F[Rate Limit Check]

            F --> G{API Status}
            G -- Available --> H[Batch Processing]
            G -- Limited --> I[Queue Hold]

            H -- Success --> J[Update Local State]
            H -- Partial --> K[Split Batch]
            H -- Failure --> L[Error Recovery]

            I --> M[Delay Timer]
            M --> F

            K --> F
            L -- Retryable --> F
            L -- Fatal --> N[Manual Resolution]
        end

        subgraph State_Management
            J --> O[Version Update]
            O --> P[Cleanup Old Data]
            P --> Q[Backup State]
        end
    ```

    6. Resource Management Flow:
    ```mermaid
    graph TD
        subgraph Resource_Monitoring
            A[System Start] --> B[Resource Check]
            B --> C{Resource Status}

            C -- OK --> D[Normal Operation]
            C -- Warning --> E[Resource Optimization]
            C -- Critical --> F[Emergency Measures]
        end

        subgraph Resource_Optimization
            E --> G[Cache Cleanup]
            E --> H[Batch Size Adjustment]
            E --> I[Queue Throttling]

            G --> J[Resource Recheck]
            H --> J
            I --> J

            J -- Improved --> D
            J -- Still Warning --> K[Further Optimization]
            J -- Worse --> F
        end

        subgraph Emergency_Handling
            F --> L[Stop New Processes]
            F --> M[Emergency Cleanup]
            F --> N[Admin Alert]

            L --> O[System Recovery]
            M --> O
            O -- Success --> P[Resume Operations]
            O -- Failure --> Q[Manual Intervention]
        end
    ```

12. Future Enhancements

    12.1 Planned Features

    12.2 Technical Improvements

    12.3 Database Enhancements

    12.4 UI/UX Improvements

13. API Documentation

    13.1 Notion API Integration

        Authentication & Authorization:
        - API Key Management:
            ```python
            from dotenv import load_dotenv
            from notion_client import Client

            load_dotenv()
            notion = Client(auth=os.getenv("NOTION_TOKEN"))
            ```

        - Token Rotation Strategy:
            * Implement 90-day token rotation
            * Store tokens in environment-specific secure storage
            * Use separate tokens for read/write operations
            * Monitor token usage and expiration

        Rate Limiting & Retry Strategy:
        - Implementation:
            ```python
            from tenacity import retry, stop_after_attempt, wait_exponential

            @retry(
                stop=stop_after_attempt(3),
                wait=wait_exponential(multiplier=1, min=4, max=10)
            )
            async def notion_api_call(self, method: str, *args, **kwargs):
                try:
                    return await getattr(self.notion, method)(*args, **kwargs)
                except APIResponseError as e:
                    if e.code == "rate_limited":
                        logger.warning(f"Rate limited: {e}")
                        raise
                    logger.error(f"API error: {e}")
                    raise
            ```

        - Rate Limits:
            * 3 requests per second per integration
            * Bucket size: 30 requests
            * Monitor usage via X-RateLimit-* headers

        Endpoint Documentation:
        1. Recipe Database Operations:
            ```python
            async def create_recipe(self, recipe: Recipe) -> str:
                """Create a new recipe page in Notion.

                Args:
                    recipe: Recipe object containing normalized data

                Returns:
                    str: Notion page ID of created recipe

                Raises:
                    NotionAPIError: If creation fails
                """
                properties = {
                    "Nombre": {"title": [{"text": {"content": recipe.title}}]},
                    "Calorías": {"number": recipe.calories},
                    "Porciones": {"number": recipe.portions},
                    "Tipo": {"select": {"name": recipe.type}},
                    "Tags": {"multi_select": [{"name": tag} for tag in recipe.tags]},
                }

                return await self.notion_api_call(
                    "pages", "create",
                    parent={"database_id": self.recipe_db_id},
                    properties=properties,
                    children=recipe.to_blocks()
                )
            ```

        2. Ingredient Database Operations:
            ```python
            async def sync_ingredients(self, ingredients: List[Ingredient]) -> Dict[str, str]:
                """Sync ingredients with Notion database.

                Args:
                    ingredients: List of ingredients to sync

                Returns:
                    Dict[str, str]: Mapping of ingredient names to Notion page IDs
                """
                existing = await self.get_existing_ingredients()
                results = {}

                for ingredient in ingredients:
                    if ingredient.name in existing:
                        results[ingredient.name] = existing[ingredient.name]
                        continue

                    page_id = await self.create_ingredient(ingredient)
                    results[ingredient.name] = page_id

                return results
            ```

        API Versioning:
        - Version Header: `Notion-Version: 2024-03-01`
        - Compatibility Matrix:
            * v1: 2024-03-01 (Current)
            * v0: 2023-09-01 (Deprecated)
        - Migration Guide for Version Updates
        - Version-specific Error Handling

        Integration Testing:
        ```python
        @pytest.mark.integration
        class TestNotionIntegration:
            @pytest.fixture(autouse=True)
            async def setup(self):
                self.client = NotionClient()
                self.test_recipe = Recipe(
                    title="Test Recipe",
                    portions=4,
                    calories=400,
                    ingredients=[...]
                )

            async def test_create_recipe(self):
                page_id = await self.client.create_recipe(self.test_recipe)
                assert page_id

                # Verify creation
                page = await self.client.get_page(page_id)
                assert page["properties"]["Nombre"]["title"][0]["text"]["content"] == "Test Recipe"
        ```

    13.2 Error Handling

        Error Codes & Messages:
        ```python
        class NotionError(Enum):
            RATE_LIMITED = ("rate_limited", "Rate limit exceeded", True)  # Retryable
            VALIDATION_ERROR = ("validation_error", "Invalid data format", False)
            AUTH_ERROR = ("unauthorized", "Invalid authentication", False)
            NOT_FOUND = ("not_found", "Resource not found", False)

            def __init__(self, code: str, message: str, retryable: bool):
                self.code = code
                self.message = message
                self.retryable = retryable
        ```

        Recovery Procedures:
        ```python
        class ErrorHandler:
            def __init__(self):
                self.error_counts = defaultdict(int)
                self.last_errors = {}

            async def handle_error(self, error: Exception, context: dict):
                error_code = self._classify_error(error)
                self.error_counts[error_code] += 1
                self.last_errors[error_code] = error

                if self._should_retry(error_code):
                    return await self._retry_operation(context)

                if self._is_critical(error_code):
                    await self._notify_critical(error, context)

                await self._log_error(error, context)

            def _classify_error(self, error: Exception) -> NotionError:
                if isinstance(error, APIResponseError):
                    return NotionError(error.code)
                return NotionError.UNKNOWN
        ```

        Notification Workflows:
        ```python
        class NotificationManager:
            def __init__(self):
                self.slack_webhook = os.getenv("SLACK_WEBHOOK")
                self.email_config = {
                    "smtp_server": os.getenv("SMTP_SERVER"),
                    "port": int(os.getenv("SMTP_PORT")),
                    "username": os.getenv("SMTP_USER"),
                    "password": os.getenv("SMTP_PASS")
                }

            async def notify_error(self, error: Exception, severity: str):
                message = self._format_error_message(error)

                if severity == "critical":
                    await self._send_slack_alert(message)
                    await self._send_email_alert(message)
                else:
                    await self._log_warning(message)
        ```

        Logging Strategy:
        ```python
        import structlog

        logger = structlog.get_logger()

        class LoggingConfig:
            @staticmethod
            def configure():
                structlog.configure(
                    processors=[
                        structlog.processors.TimeStamper(fmt="iso"),
                        structlog.processors.StackInfoRenderer(),
                        structlog.processors.format_exc_info,
                        structlog.processors.JSONRenderer()
                    ],
                    context_class=dict,
                    logger_factory=structlog.PrintLoggerFactory(),
                    wrapper_class=structlog.BoundLogger,
                    cache_logger_on_first_use=True,
                )

            @staticmethod
            def log_request(request_id: str, **kwargs):
                logger.info(
                    "api_request",
                    request_id=request_id,
                    **kwargs
                )

            @staticmethod
            def log_error(error: Exception, **context):
                logger.error(
                    "error_occurred",
                    error_type=type(error).__name__,
                    error_message=str(error),
                    **context
                )
        ```

        Implementation Example:
        ```python
        class NotionManager:
            def __init__(self):
                self.error_handler = ErrorHandler()
                self.notification_manager = NotificationManager()
                LoggingConfig.configure()

            async def safe_api_call(self, operation: Callable, *args, **kwargs):
                request_id = str(uuid.uuid4())
                LoggingConfig.log_request(request_id, operation=operation.__name__)

                try:
                    return await operation(*args, **kwargs)
                except Exception as e:
                    context = {
                        "request_id": request_id,
                        "operation": operation.__name__,
                        "args": args,
                        "kwargs": kwargs
                    }
                    await self.error_handler.handle_error(e, context)
                    raise
        ```

14. Deployment & Infrastructure
    14.1 Deployment Guide

        Environment Setup:
        1. Development Environment:
        ```bash
        # Create and activate virtual environment
        python -m venv .venv
        source .venv/bin/activate

        # Install dependencies
        pip install -r requirements.txt

        # Set up pre-commit hooks
        pre-commit install

        # Configure environment variables
        cp .env.example .env
        ```

        2. Container Configuration:
        ```dockerfile
        # Dockerfile
        FROM python:3.13-slim

        # Set working directory
        WORKDIR /app

        # Install system dependencies
        RUN apt-get update && apt-get install -y \
            tesseract-ocr \
            libpoppler-cpp-dev \
            && rm -rf /var/lib/apt/lists/*

        # Copy requirements and install Python dependencies
        COPY requirements.txt .
        RUN pip install --no-cache-dir -r requirements.txt

        # Copy application code
        COPY . .

        # Set environment variables
        ENV PYTHONPATH=/app
        ENV PYTHONUNBUFFERED=1

        # Run the application
        CMD ["python", "main.py"]
        ```
