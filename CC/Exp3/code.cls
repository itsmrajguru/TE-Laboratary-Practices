/*
================================================================================
ASSIGNMENT 3: Creating an Application in Salesforce.com using Apex Programming Language
Subject: Cloud Computing (CC)
University: Savitribai Phule Pune University (SPPU)
Course: Third Year Computer Engineering (2019 Course)
================================================================================

PART 1 - THEORY
================================================================================

1. WHAT IS SALESFORCE?
------------------------
Salesforce is a cloud-based Customer Relationship Management (CRM) platform
that helps businesses manage their relationships and interactions with customers
and potential customers. It is one of the world's leading SaaS (Software as a
Service) platforms.

Salesforce offers multiple cloud products:
  - Sales Cloud     : Manage sales pipeline, leads, opportunities
  - Service Cloud   : Customer support and helpdesk
  - Marketing Cloud : Email campaigns and marketing automation
  - Commerce Cloud  : E-commerce solutions
  - App Cloud       : Build custom applications (uses Apex + Lightning)

2. WHAT IS APEX?
-----------------
Apex is a strongly typed, object-oriented programming language developed by
Salesforce. It allows developers to write custom business logic that runs on
the Salesforce platform (Force.com).

Key Characteristics of Apex:
  - Syntax similar to Java
  - Runs on Salesforce servers (multi-tenant cloud environment)
  - Tightly integrated with Salesforce database (SOQL/SOSL queries)
  - Supports triggers, classes, interfaces, and test classes
  - Executed in a governor limits environment (to prevent resource abuse
    in a multi-tenant setup)

3. APEX vs JAVA vs PYTHON
---------------------------
  Feature              | Apex            | Java            | Python
  ---------------------|-----------------|-----------------|----------------
  Type System          | Strongly typed  | Strongly typed  | Dynamically typed
  Platform             | Salesforce only | Any JVM         | Any OS
  Database Query       | SOQL inline     | JDBC/ORM        | ORM/raw SQL
  Cloud Native         | Yes             | No              | No
  Trigger Support      | Built-in        | No              | No
  Governor Limits      | Yes             | No              | No

4. GOVERNOR LIMITS IN APEX
----------------------------
Since Salesforce is a multi-tenant platform (many companies share same servers),
Apex enforces "Governor Limits" to ensure no single app monopolizes resources:

  - Max 100 SOQL queries per transaction
  - Max 50,000 records returned by SOQL
  - Max 150 DML statements per transaction
  - Max 10,000 records processed by DML
  - Max CPU time: 10,000ms per transaction
  - Max heap size: 6MB per transaction

5. SALESFORCE DATABASE CONCEPTS
---------------------------------
Salesforce uses its own database called Force.com database.
  - Objects   = Tables in traditional database
  - Fields    = Columns
  - Records   = Rows
  - SOQL      = Salesforce Object Query Language (like SQL for Salesforce)

Standard Objects (pre-built by Salesforce):
  - Account   : Companies or organizations
  - Contact   : Individual people
  - Lead      : Potential customers
  - Opportunity: Potential sales deals
  - Case      : Customer support issues

Custom Objects (you create these):
  - Defined with __c suffix: e.g., Job_Application__c, Student__c

6. SOQL - SALESFORCE OBJECT QUERY LANGUAGE
--------------------------------------------
SOQL is similar to SQL but used to query Salesforce objects:

  SQL   : SELECT name, age FROM students WHERE age > 20
  SOQL  : SELECT Name, Age__c FROM Student__c WHERE Age__c > 20

Key differences from SQL:
  - No JOIN keyword (use relationship queries instead)
  - Cannot query multiple objects in one query (no UNION)
  - All custom field names end with __c
  - Relationship traversal: SELECT Account.Name FROM Contact

7. APEX TRIGGERS
-----------------
Triggers are Apex code that executes automatically before or after
data manipulation events (insert, update, delete, undelete).

Trigger Events:
  - before insert  : Before a record is saved
  - after insert   : After a record is saved
  - before update  : Before an existing record is updated
  - after update   : After an existing record is updated
  - before delete  : Before a record is deleted
  - after delete   : After a record is deleted

Trigger Context Variables:
  - Trigger.new     : List of new records
  - Trigger.old     : List of old records (before change)
  - Trigger.isInsert: True if insert operation
  - Trigger.isUpdate: True if update operation

8. APEX CLASSES
----------------
Apex classes are similar to Java classes. They can have:
  - Variables (properties)
  - Methods (functions)
  - Constructors
  - Inner classes
  - Static methods

Access Modifiers:
  - public    : Accessible from anywhere
  - private   : Only within the class
  - protected : Within class and subclasses
  - global    : Accessible across namespaces (used in web services)

9. DML OPERATIONS IN APEX
---------------------------
DML (Data Manipulation Language) operations in Apex:
  - insert  : Add new records
  - update  : Modify existing records
  - delete  : Remove records
  - upsert  : Insert or update (based on external ID)
  - merge   : Merge duplicate records
  - undelete: Restore deleted records from recycle bin

10. APEX TEST CLASSES
----------------------
Salesforce requires at least 75% code coverage by test classes before
deploying to production.

  @isTest annotation marks a class as a test class
  Test.startTest() and Test.stopTest() isolate governor limits for tests
  System.assert() / System.assertEquals() used for assertions

11. STEPS TO CREATE AN APEX APPLICATION IN SALESFORCE
-------------------------------------------------------
Step 1: Create a Salesforce Developer Account
  - Go to: https://developer.salesforce.com/signup
  - Sign up for free Developer Edition org

Step 2: Access Developer Console
  - Login → Click gear icon (⚙) → Developer Console
  - OR use: Setup → Apex Classes

Step 3: Create Custom Object (if needed)
  - Setup → Object Manager → Create → Custom Object
  - Add custom fields

Step 4: Write Apex Class
  - Developer Console → File → New → Apex Class

Step 5: Write Apex Trigger (if needed)
  - Developer Console → File → New → Apex Trigger

Step 6: Execute Anonymous Apex (for testing)
  - Developer Console → Debug → Open Execute Anonymous Window

Step 7: Run Test Classes
  - Developer Console → Test → New Run → select test class

12. ADVANTAGES OF APEX ON SALESFORCE CLOUD
--------------------------------------------
  - No infrastructure management (pure PaaS)
  - Tight integration with CRM data
  - Automatic scalability
  - Built-in security (field-level, object-level security)
  - Version control through Change Sets / Salesforce DX

13. USE CASES OF APEX
-----------------------
  - Auto-assign leads to sales reps based on geography
  - Send email notifications when a deal is closed
  - Validate data before saving to database
  - Calculate discounts based on business rules
  - Integrate Salesforce with external REST APIs

================================================================================
PART 2 - IMPLEMENTATION
================================================================================

APPLICATION: Student Job Application Tracker
----------------------------------------------
We will create:
  1. Custom Object     : Job_Application__c  (stores job applications)
  2. Apex Class        : JobApplicationManager (business logic)
  3. Apex Trigger      : JobApplicationTrigger (auto-actions on save)
  4. Test Class        : JobApplicationManagerTest (for code coverage)

Files in this submission:
  - JobApplicationManager.cls      (Main Apex Class)
  - JobApplicationTrigger.trigger  (Trigger)
  - JobApplicationManagerTest.cls  (Test Class)

================================================================================
*/


/* ─────────────────────────────────────────────────────────────────
   FILE 1: JobApplicationManager.cls
   This is the main Apex class containing all business logic.
   Think of it like a Service class in Spring Boot or Node.js.
   ───────────────────────────────────────────────────────────────── */

public class JobApplicationManager {

    /* ─────────────────────────────────────────────────────────────
       METHOD 1: createApplication()
       Creates a new Job Application record in Salesforce database.
       Parameters:
         - studentName : Name of the student applying
         - companyName : Company they are applying to
         - jobRole     : Role/position they applied for
       Returns: The inserted Job_Application__c record
       ───────────────────────────────────────────────────────────── */
    public static Job_Application__c createApplication(
        String studentName,
        String companyName,
        String jobRole
    ) {
        // Create a new instance of the custom object Job_Application__c
        // This is like creating a new document/row before saving it
        Job_Application__c newApp = new Job_Application__c();

        // Set the field values on the new record
        // __c suffix means these are custom fields we created
        newApp.Student_Name__c   = studentName;
        newApp.Company_Name__c   = companyName;
        newApp.Job_Role__c       = jobRole;
        newApp.Status__c         = 'Applied';         // Default status on creation
        newApp.Applied_Date__c   = Date.today();      // Auto-set today's date

        // insert — DML operation to save the record to Salesforce DB
        // This is equivalent to db.save() in Mongoose or .save() in Django
        insert newApp;

        // Return the saved record (now has an Id assigned by Salesforce)
        return newApp;
    }


    /* ─────────────────────────────────────────────────────────────
       METHOD 2: getApplicationsByStudent()
       Fetches all job applications for a specific student.
       Uses SOQL (Salesforce Object Query Language) to query DB.
       Parameters:
         - studentName : Name of the student to search for
       Returns: List of Job_Application__c records
       ───────────────────────────────────────────────────────────── */
    public static List<Job_Application__c> getApplicationsByStudent(String studentName) {

        // SOQL query — similar to SQL SELECT statement
        // We query the custom object Job_Application__c
        // WHERE filters by student name
        // ORDER BY sorts by applied date (newest first)
        List<Job_Application__c> applications = [
            SELECT
                Id,                  // Unique Salesforce record ID
                Student_Name__c,     // Student name field
                Company_Name__c,     // Company name field
                Job_Role__c,         // Job role/position field
                Status__c,           // Current application status
                Applied_Date__c      // Date of application
            FROM
                Job_Application__c   // Custom object (table)
            WHERE
                Student_Name__c = :studentName   // :studentName is a bind variable (prevents SOQL injection)
            ORDER BY
                Applied_Date__c DESC             // Newest applications first
        ];

        return applications;
    }


    /* ─────────────────────────────────────────────────────────────
       METHOD 3: updateApplicationStatus()
       Updates the status of a specific job application.
       Valid statuses: Applied, Interview Scheduled, Selected, Rejected
       Parameters:
         - applicationId : The Salesforce record Id of the application
         - newStatus     : The new status to set
       ───────────────────────────────────────────────────────────── */
    public static void updateApplicationStatus(Id applicationId, String newStatus) {

        // Valid status values (like an enum validation)
        List<String> validStatuses = new List<String>{
            'Applied',
            'Interview Scheduled',
            'Selected',
            'Rejected'
        };

        // Check if the provided status is valid
        if (!validStatuses.contains(newStatus)) {
            // AuraHandledException is used to send error messages to UI
            throw new AuraHandledException('Invalid status: ' + newStatus +
                '. Valid values are: ' + String.join(validStatuses, ', '));
        }

        // Query the specific record by its Id
        // LIMIT 1 — we only want one record
        Job_Application__c app = [
            SELECT Id, Status__c, Student_Name__c, Company_Name__c
            FROM Job_Application__c
            WHERE Id = :applicationId
            LIMIT 1
        ];

        // Update the status field on the fetched record
        app.Status__c = newStatus;

        // update DML — saves the changes back to Salesforce DB
        update app;

        // Send email notification if candidate is selected
        // (calls the helper method below)
        if (newStatus == 'Selected') {
            sendSelectionEmail(app.Student_Name__c, app.Company_Name__c);
        }
    }


    /* ─────────────────────────────────────────────────────────────
       METHOD 4: getApplicationStats()
       Returns a summary/statistics of all applications.
       Uses SOQL aggregate functions (COUNT, GROUP BY).
       Returns: Map of status → count
       ───────────────────────────────────────────────────────────── */
    public static Map<String, Integer> getApplicationStats() {

        // AggregateResult is used when SOQL uses GROUP BY
        // COUNT(Id) counts records per group
        List<AggregateResult> results = [
            SELECT Status__c, COUNT(Id) total
            FROM Job_Application__c
            GROUP BY Status__c
        ];

        // Map to store status → count pairs
        // Like a JavaScript object: { "Applied": 5, "Selected": 2 }
        Map<String, Integer> statsMap = new Map<String, Integer>();

        // Loop through aggregate results and populate the map
        for (AggregateResult ar : results) {
            // get('Status__c') fetches the grouped field value
            // get('total') fetches the COUNT result
            String status = (String) ar.get('Status__c');
            Integer count  = (Integer) ar.get('total');
            statsMap.put(status, count);
        }

        return statsMap;
    }


    /* ─────────────────────────────────────────────────────────────
       METHOD 5: deleteApplication() [private helper]
       Deletes a job application record.
       Parameters:
         - applicationId : Record Id to delete
       ───────────────────────────────────────────────────────────── */
    public static void deleteApplication(Id applicationId) {

        // Query the record first (need the object to delete it)
        Job_Application__c app = [
            SELECT Id
            FROM Job_Application__c
            WHERE Id = :applicationId
            LIMIT 1
        ];

        // delete DML — removes the record (goes to Recycle Bin)
        delete app;
    }


    /* ─────────────────────────────────────────────────────────────
       HELPER METHOD: sendSelectionEmail()
       Sends an email notification when a student is selected.
       private — only callable within this class
       ───────────────────────────────────────────────────────────── */
    private static void sendSelectionEmail(String studentName, String companyName) {

        // Messaging.SingleEmailMessage is Salesforce's built-in email class
        Messaging.SingleEmailMessage mail = new Messaging.SingleEmailMessage();

        // Set recipient — in real app, fetch student's actual email from DB
        mail.setToAddresses(new List<String>{'hr@' + companyName.toLowerCase().replaceAll(' ', '') + '.com'});

        // Set email subject
        mail.setSubject('Congratulations! ' + studentName + ' Selected at ' + companyName);

        // Set email body
        mail.setPlainTextBody(
            'Dear HR Team,\n\n' +
            'This is to inform you that ' + studentName +
            ' has been marked as SELECTED for a position at ' + companyName + '.\n\n' +
            'Please proceed with the offer letter process.\n\n' +
            'Regards,\nJob Application System'
        );

        // sendEmail() sends the email — Salesforce handles delivery
        Messaging.sendEmail(new List<Messaging.SingleEmailMessage>{ mail });
    }
}


/* ─────────────────────────────────────────────────────────────────
   FILE 2: JobApplicationTrigger.trigger
   Triggers run automatically when records are inserted/updated/deleted.
   This trigger fires BEFORE insert to validate data and
   AFTER insert to log activity.
   ───────────────────────────────────────────────────────────── */

/*
trigger JobApplicationTrigger on Job_Application__c (before insert, before update, after insert) {

    // ── BEFORE INSERT: Runs before new records are saved ──
    // Use this to validate or auto-populate fields
    if (Trigger.isBefore && Trigger.isInsert) {

        // Trigger.new = list of all records being inserted
        for (Job_Application__c app : Trigger.new) {

            // Validation: Student name cannot be empty
            if (String.isBlank(app.Student_Name__c)) {
                // addError() prevents the insert and shows error to user
                app.Student_Name__c.addError('Student Name is required.');
            }

            // Validation: Company name cannot be empty
            if (String.isBlank(app.Company_Name__c)) {
                app.Company_Name__c.addError('Company Name is required.');
            }

            // Auto-set Applied Date to today if not provided
            if (app.Applied_Date__c == null) {
                app.Applied_Date__c = Date.today();
            }

            // Auto-set default status to 'Applied' if not set
            if (String.isBlank(app.Status__c)) {
                app.Status__c = 'Applied';
            }
        }
    }

    // ── BEFORE UPDATE: Runs before existing records are updated ──
    if (Trigger.isBefore && Trigger.isUpdate) {

        for (Job_Application__c app : Trigger.new) {
            // Get the old version of the record (before update)
            Job_Application__c oldApp = Trigger.oldMap.get(app.Id);

            // Business Rule: Once 'Selected', status cannot be changed back to 'Applied'
            if (oldApp.Status__c == 'Selected' && app.Status__c == 'Applied') {
                app.Status__c.addError('Cannot revert status from Selected to Applied.');
            }
        }
    }

    // ── AFTER INSERT: Runs after records are successfully saved ──
    if (Trigger.isAfter && Trigger.isInsert) {

        // Collect all IDs of newly inserted applications
        List<Id> newAppIds = new List<Id>();
        for (Job_Application__c app : Trigger.new) {
            newAppIds.add(app.Id);
        }

        // You can call other classes here for post-insert logic
        // e.g., send welcome email, create follow-up tasks, etc.
        System.debug('New Job Applications created with IDs: ' + newAppIds);
    }
}
*/


/* ─────────────────────────────────────────────────────────────────
   FILE 3: JobApplicationManagerTest.cls
   Test class — required for deployment (must have 75%+ coverage).
   @isTest annotation marks this as a test class.
   Test classes do NOT count against governor limits.
   ───────────────────────────────────────────────────────────── */

/*
@isTest
private class JobApplicationManagerTest {

    // ── TEST 1: Test creating a new application ──
    @isTest
    static void testCreateApplication() {

        // Test.startTest() resets governor limits for test isolation
        Test.startTest();

        // Call the method we want to test
        Job_Application__c result = JobApplicationManager.createApplication(
            'Mangesh Patil',        // Student name
            'Infosys',             // Company
            'Software Engineer'    // Role
        );

        // Test.stopTest() ensures async operations complete
        Test.stopTest();

        // System.assertNotNull checks the result is not null
        System.assertNotNull(result.Id, 'Application should have been created with an Id');

        // System.assertEquals checks expected vs actual value
        System.assertEquals('Applied', result.Status__c, 'Default status should be Applied');
        System.assertEquals('Mangesh Patil', result.Student_Name__c, 'Student name should match');
    }


    // ── TEST 2: Test fetching applications by student ──
    @isTest
    static void testGetApplicationsByStudent() {

        // First, create some test data
        // In test classes, data is isolated — doesn't affect real data
        Job_Application__c app1 = new Job_Application__c(
            Student_Name__c = 'Mangesh Patil',
            Company_Name__c = 'TCS',
            Job_Role__c     = 'Developer',
            Status__c       = 'Applied',
            Applied_Date__c = Date.today()
        );

        Job_Application__c app2 = new Job_Application__c(
            Student_Name__c = 'Mangesh Patil',
            Company_Name__c = 'Wipro',
            Job_Role__c     = 'Analyst',
            Status__c       = 'Interview Scheduled',
            Applied_Date__c = Date.today()
        );

        // Insert both records
        insert new List<Job_Application__c>{ app1, app2 };

        Test.startTest();
        // Fetch applications for the student
        List<Job_Application__c> results = JobApplicationManager.getApplicationsByStudent('Mangesh Patil');
        Test.stopTest();

        // There should be exactly 2 applications
        System.assertEquals(2, results.size(), 'Should return 2 applications for Mangesh Patil');
    }


    // ── TEST 3: Test status update ──
    @isTest
    static void testUpdateApplicationStatus() {

        // Create a test application
        Job_Application__c app = new Job_Application__c(
            Student_Name__c = 'Rahul Sharma',
            Company_Name__c = 'Google',
            Job_Role__c     = 'SDE',
            Status__c       = 'Applied',
            Applied_Date__c = Date.today()
        );
        insert app;

        Test.startTest();
        // Update status to 'Interview Scheduled'
        JobApplicationManager.updateApplicationStatus(app.Id, 'Interview Scheduled');
        Test.stopTest();

        // Re-query the record to verify the update
        Job_Application__c updatedApp = [
            SELECT Status__c FROM Job_Application__c WHERE Id = :app.Id
        ];

        System.assertEquals('Interview Scheduled', updatedApp.Status__c,
            'Status should be updated to Interview Scheduled');
    }


    // ── TEST 4: Test invalid status throws error ──
    @isTest
    static void testInvalidStatusThrowsError() {

        Job_Application__c app = new Job_Application__c(
            Student_Name__c = 'Test Student',
            Company_Name__c = 'Test Co',
            Job_Role__c     = 'Tester',
            Status__c       = 'Applied',
            Applied_Date__c = Date.today()
        );
        insert app;

        Test.startTest();

        // We expect an exception to be thrown for invalid status
        try {
            JobApplicationManager.updateApplicationStatus(app.Id, 'InvalidStatus');
            // If no exception, test should fail
            System.assert(false, 'Expected an exception for invalid status');
        } catch (AuraHandledException e) {
            // Exception was thrown — this is the expected behavior
            System.assert(e.getMessage().contains('Invalid status'),
                'Exception message should mention invalid status');
        }

        Test.stopTest();
    }
}
*/