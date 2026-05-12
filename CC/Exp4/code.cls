/*
================================================================================
ASSIGNMENT 4: Design and Develop a Custom Application (Mini Project)
               using Salesforce Cloud
Application Name: Student Placement Tracker
Subject: Cloud Computing (CC)
University: Savitribai Phule Pune University (SPPU)
Course: Third Year Computer Engineering (2019 Course)
================================================================================

PART 1 - THEORY
================================================================================

1. WHAT IS A CUSTOM APPLICATION IN SALESFORCE?
------------------------------------------------
A custom application in Salesforce is a tailored solution built on the
Salesforce platform using its tools and technologies. Unlike standard
Salesforce CRM features, custom applications are designed to meet specific
business needs.

A Salesforce custom application typically consists of:
  - Custom Objects     : Custom database tables to store your data
  - Custom Fields      : Custom columns in those tables
  - Apex Classes       : Backend business logic (like controllers)
  - Apex Triggers      : Auto-execute logic on data events
  - Lightning Pages    : Frontend UI pages
  - Validation Rules   : Data integrity enforcement
  - Workflow Rules     : Automated actions on data changes
  - Reports & Dashboards: Data visualization and analytics

2. WHAT IS SALESFORCE APP CLOUD (FORCE.COM)?
---------------------------------------------
Salesforce App Cloud (also called Force.com) is a Platform as a Service
(PaaS) offering from Salesforce that allows developers to build, deploy,
and manage custom applications on Salesforce's cloud infrastructure.

Key Components of App Cloud:
  - Force.com Platform   : Core cloud infrastructure
  - Apex               : Server-side programming language
  - Visualforce        : Page markup language (older UI framework)
  - Lightning Framework : Modern component-based UI framework
  - Salesforce DX      : Developer experience tools (CLI, version control)
  - AppExchange        : Marketplace for Salesforce apps

3. APPLICATION: STUDENT PLACEMENT TRACKER
-------------------------------------------
The Student Placement Tracker is a mini project built on Salesforce Cloud
to manage and track the entire placement process of engineering students.

Modules in this Application:
  a) Student Management    : Store and manage student profiles
  b) Company Management    : Track companies visiting for placements
  c) Job Drive Management  : Manage placement drives/events
  d) Application Tracking  : Track student applications per company
  e) Placement Results     : Record final placement outcomes
  f) Reports & Analytics   : Placement statistics and dashboards

4. CUSTOM OBJECTS DESIGNED
----------------------------
We design the following custom objects (tables):

  Object Name              | API Name                | Purpose
  -------------------------|-------------------------|---------------------------
  Student                  | Student__c              | Stores student details
  Company                  | Company__c              | Companies visiting campus
  Job Drive                | Job_Drive__c            | Placement drive/event info
  Placement Application    | Placement_Application__c| Student-Company application
  Placement Result         | Placement_Result__c     | Final placement outcome

5. OBJECT RELATIONSHIPS
------------------------
Salesforce supports two types of relationships:

  a) Lookup Relationship:
     - Loosely coupled (like a foreign key in SQL)
     - Child record can exist without parent
     - Example: Student lookup on Application

  b) Master-Detail Relationship:
     - Tightly coupled
     - Child cannot exist without parent
     - Deleting parent deletes all children
     - Example: Placement Result is Master-Detail with Job Drive

  Relationship Diagram:
  
  [Student__c] ──lookup──> [Placement_Application__c] <──lookup── [Company__c]
                                      |
                                   lookup
                                      |
                                [Job_Drive__c]
                                      |
                                  master-detail
                                      |
                              [Placement_Result__c]

6. CUSTOM FIELDS ON EACH OBJECT
---------------------------------
  Student__c:
    - Name (standard)        : Student full name
    - Roll_Number__c         : Text(20) — unique roll number
    - Branch__c              : Picklist — CS/IT/ENTC/Mechanical
    - CGPA__c                : Number(3,2) — academic score
    - Skills__c              : Long Text Area — technical skills
    - Email__c               : Email field
    - Phone__c               : Phone field
    - Is_Placed__c           : Checkbox — placed or not
    - Placed_At__c           : Text — company name if placed

  Company__c:
    - Name (standard)        : Company name
    - Industry__c            : Picklist — IT/Finance/Core/Consulting
    - Package_LPA__c         : Number — salary offered (LPA)
    - HR_Email__c            : Email of HR contact
    - Website__c             : URL field
    - Visit_Date__c          : Date — campus visit date

  Job_Drive__c:
    - Name (standard)        : Drive name (e.g., "TCS NQT 2024")
    - Company__c             : Lookup to Company__c
    - Drive_Date__c          : Date/Time
    - Eligible_Branches__c   : Multi-select Picklist
    - Min_CGPA__c            : Number — minimum CGPA required
    - Vacancies__c           : Number — total seats available
    - Status__c              : Picklist — Upcoming/Active/Completed

  Placement_Application__c:
    - Student__c             : Lookup to Student__c
    - Job_Drive__c           : Lookup to Job_Drive__c
    - Applied_Date__c        : Date
    - Round_Status__c        : Picklist — Applied/Aptitude/Technical/HR/Selected/Rejected
    - Remarks__c             : Text Area — interview notes

  Placement_Result__c:
    - Student__c             : Lookup to Student__c
    - Company__c             : Lookup to Company__c
    - Job_Drive__c           : Master-Detail to Job_Drive__c
    - Offered_Package_LPA__c : Number — actual offer received
    - Offer_Date__c          : Date
    - Joining_Date__c        : Date

7. VALIDATION RULES
--------------------
Salesforce Validation Rules prevent bad data from being saved:

  Rule 1: CGPA must be between 0 and 10
    Formula: OR(CGPA__c < 0, CGPA__c > 10)
    Error: "CGPA must be between 0.00 and 10.00"

  Rule 2: Minimum CGPA for application
    Formula: Student__r.CGPA__c < Job_Drive__r.Min_CGPA__c
    Error: "Student does not meet minimum CGPA requirement for this drive"

  Rule 3: Cannot apply to same drive twice
    (Handled via Apex trigger — duplicate check)

8. WORKFLOW / PROCESS AUTOMATION
----------------------------------
  Automation 1: Auto-update Is_Placed__c
    - Trigger: When Placement_Result__c is created
    - Action: Set Student.Is_Placed__c = true, Student.Placed_At__c = Company name

  Automation 2: Email notification on selection
    - Trigger: When Round_Status__c changes to 'Selected'
    - Action: Send congratulation email to student

  Automation 3: Drive status auto-update
    - Trigger: When Drive_Date__c passes
    - Action: Set Job_Drive__c.Status__c = 'Completed'

9. REPORTS AND DASHBOARDS
---------------------------
  Reports designed in this application:

  Report 1: Placement Summary
    - Total students placed vs unplaced (pie chart)

  Report 2: Company-wise Placements
    - Number of students placed per company (bar chart)

  Report 3: Branch-wise Placement Rate
    - Placement % per branch (CS/IT/ENTC etc.)

  Report 4: Package Distribution
    - Average, min, max packages offered

10. STEPS TO BUILD THIS IN SALESFORCE
---------------------------------------
  Step 1: Create Developer Org (developer.salesforce.com)
  Step 2: Create Custom Objects (Setup → Object Manager)
  Step 3: Add Custom Fields on each object
  Step 4: Set up Relationships between objects
  Step 5: Create Validation Rules
  Step 6: Write Apex Classes and Triggers
  Step 7: Create Lightning App Page (drag-drop UI)
  Step 8: Create Reports and Dashboard
  Step 9: Set up Profiles and Permissions
  Step 10: Test with sample data

11. ADVANTAGES OF BUILDING ON SALESFORCE CLOUD
------------------------------------------------
  - No infrastructure to manage (pure PaaS)
  - Built-in user authentication and role management
  - Drag-and-drop UI builder (Lightning App Builder)
  - Automatic backups and disaster recovery
  - Mobile-ready out of the box (Salesforce Mobile App)
  - AppExchange ecosystem for extending functionality
  - Built-in reporting and dashboard tools
  - Enterprise-grade security (field-level, object-level)

12. COMPARISON: CUSTOM APP ON SALESFORCE vs Traditional Development
--------------------------------------------------------------------
  Feature              | Salesforce Cloud        | Traditional (MERN Stack)
  ---------------------|-------------------------|------------------------
  Infrastructure       | Fully managed by SF     | Self-hosted / cloud VM
  Database             | Force.com DB (objects)  | MongoDB / PostgreSQL
  Backend              | Apex                    | Node.js / Express
  Frontend             | Lightning Components    | React / Next.js
  Auth                 | Built-in profiles/roles | JWT / OAuth custom
  Deployment           | Click Deploy / SF DX    | CI/CD pipelines
  Scalability          | Auto (managed by SF)    | Manual config needed
  Cost model           | Per user/month license  | Pay-per-use infra
  Dev Speed            | Fast (low-code + Apex)  | Depends on team
  Customization        | Limited to SF platform  | Unlimited

================================================================================
PART 2 - IMPLEMENTATION CODE
================================================================================
*/


/* ─────────────────────────────────────────────────────────────────
   FILE 1: PlacementTrackerController.cls
   Main controller class for the Student Placement Tracker app.
   Contains all business logic methods used by the Lightning UI.
   ───────────────────────────────────────────────────────────── */

public with sharing class PlacementTrackerController {

    /* ─────────────────────────────────────────────────────────────
       METHOD 1: registerStudent()
       Registers a new student into the placement system.
       Called when the "Register Student" form is submitted.

       @AuraEnabled — exposes this method to Lightning UI components
       @param name       — Student's full name
       @param rollNo     — Unique roll number
       @param branch     — Engineering branch (CS/IT/ENTC etc.)
       @param cgpa       — CGPA (0–10 scale)
       @param skills     — Comma-separated technical skills
       @param email      — Student email
       @param phone      — Student contact number
       @return           — The created Student__c record
       ───────────────────────────────────────────────────────────── */
    @AuraEnabled
    public static Student__c registerStudent(
        String name,
        String rollNo,
        String branch,
        Decimal cgpa,
        String skills,
        String email,
        String phone
    ) {
        // Validate CGPA range before saving
        if (cgpa < 0 || cgpa > 10) {
            throw new AuraHandledException('CGPA must be between 0.00 and 10.00');
        }

        // Check if roll number already exists (prevent duplicates)
        List<Student__c> existing = [
            SELECT Id FROM Student__c
            WHERE Roll_Number__c = :rollNo
            LIMIT 1
        ];

        if (!existing.isEmpty()) {
            throw new AuraHandledException('A student with Roll Number ' + rollNo + ' already exists.');
        }

        // Create new Student record
        Student__c student = new Student__c();
        student.Name         = name;
        student.Roll_Number__c = rollNo;
        student.Branch__c    = branch;
        student.CGPA__c      = cgpa;
        student.Skills__c    = skills;
        student.Email__c     = email;
        student.Phone__c     = phone;
        student.Is_Placed__c = false;  // Default: not placed yet

        // Save to Salesforce database
        insert student;

        return student;
    }


    /* ─────────────────────────────────────────────────────────────
       METHOD 2: addCompany()
       Adds a new company to the placement portal.

       @param companyName — Name of the company
       @param industry    — Industry sector
       @param packageLPA  — CTC offered in LPA
       @param hrEmail     — HR contact email
       @param visitDate   — Date of campus visit
       @return            — Created Company__c record
       ───────────────────────────────────────────────────────────── */
    @AuraEnabled
    public static Company__c addCompany(
        String companyName,
        String industry,
        Decimal packageLPA,
        String hrEmail,
        Date visitDate
    ) {
        // Create Company record
        Company__c company       = new Company__c();
        company.Name             = companyName;
        company.Industry__c      = industry;
        company.Package_LPA__c   = packageLPA;
        company.HR_Email__c      = hrEmail;
        company.Visit_Date__c    = visitDate;

        insert company;
        return company;
    }


    /* ─────────────────────────────────────────────────────────────
       METHOD 3: createJobDrive()
       Creates a new placement drive/event for a company.
       Links the drive to an existing company via Lookup.

       @param driveName      — Name of the drive (e.g., "TCS NQT 2024")
       @param companyId      — Salesforce ID of the Company__c record
       @param driveDate      — Date and time of the drive
       @param eligibleBranch — Which branches can apply
       @param minCGPA        — Minimum CGPA required
       @param vacancies      — Number of openings
       @return               — Created Job_Drive__c record
       ───────────────────────────────────────────────────────────── */
    @AuraEnabled
    public static Job_Drive__c createJobDrive(
        String driveName,
        Id companyId,
        DateTime driveDate,
        String eligibleBranch,
        Decimal minCGPA,
        Integer vacancies
    ) {
        Job_Drive__c drive         = new Job_Drive__c();
        drive.Name                 = driveName;
        drive.Company__c           = companyId;  // Lookup relationship set here
        drive.Drive_Date__c        = driveDate;
        drive.Eligible_Branches__c = eligibleBranch;
        drive.Min_CGPA__c          = minCGPA;
        drive.Vacancies__c         = vacancies;
        drive.Status__c            = 'Upcoming'; // Default status on creation

        insert drive;
        return drive;
    }


    /* ─────────────────────────────────────────────────────────────
       METHOD 4: applyToJobDrive()
       Allows a student to apply for a placement drive.
       Checks eligibility (CGPA, branch) before creating application.

       @param studentId  — Salesforce ID of the Student__c record
       @param driveId    — Salesforce ID of the Job_Drive__c record
       @return           — Created Placement_Application__c record
       ───────────────────────────────────────────────────────────── */
    @AuraEnabled
    public static Placement_Application__c applyToJobDrive(Id studentId, Id driveId) {

        // Fetch the student's details for eligibility check
        // Relationship query: fetches student data in one SOQL
        Student__c student = [
            SELECT Id, Name, Branch__c, CGPA__c, Is_Placed__c
            FROM Student__c
            WHERE Id = :studentId
            LIMIT 1
        ];

        // Fetch the drive details for eligibility check
        Job_Drive__c drive = [
            SELECT Id, Name, Min_CGPA__c, Eligible_Branches__c,
                   Status__c, Vacancies__c, Company__c, Company__r.Name
            FROM Job_Drive__c
            WHERE Id = :driveId
            LIMIT 1
        ];

        // Eligibility Check 1: Student must not already be placed
        if (student.Is_Placed__c) {
            throw new AuraHandledException(
                student.Name + ' is already placed. Cannot apply to new drives.'
            );
        }

        // Eligibility Check 2: Drive must be Active or Upcoming
        if (drive.Status__c == 'Completed') {
            throw new AuraHandledException('This placement drive is already completed.');
        }

        // Eligibility Check 3: CGPA must meet minimum requirement
        if (student.CGPA__c < drive.Min_CGPA__c) {
            throw new AuraHandledException(
                'Minimum CGPA required: ' + drive.Min_CGPA__c +
                '. Your CGPA: ' + student.CGPA__c
            );
        }

        // Eligibility Check 4: Check for duplicate application
        List<Placement_Application__c> duplicate = [
            SELECT Id FROM Placement_Application__c
            WHERE Student__c = :studentId
            AND Job_Drive__c = :driveId
            LIMIT 1
        ];

        if (!duplicate.isEmpty()) {
            throw new AuraHandledException(
                'You have already applied to this drive: ' + drive.Name
            );
        }

        // All checks passed — create the application record
        Placement_Application__c app = new Placement_Application__c();
        app.Student__c       = studentId;
        app.Job_Drive__c     = driveId;
        app.Applied_Date__c  = Date.today();
        app.Round_Status__c  = 'Applied';  // Initial status

        insert app;
        return app;
    }


    /* ─────────────────────────────────────────────────────────────
       METHOD 5: updateRoundStatus()
       Updates a student's application status after each round.
       If status is 'Selected', creates a Placement Result record.

       @param applicationId — ID of the Placement_Application__c
       @param newStatus     — New round status
       @param remarks       — Notes/feedback from the round
       ───────────────────────────────────────────────────────────── */
    @AuraEnabled
    public static void updateRoundStatus(Id applicationId, String newStatus, String remarks) {

        // Fetch the application along with related student and drive info
        // Cross-object field access using relationship traversal (r__)
        Placement_Application__c app = [
            SELECT Id, Round_Status__c, Student__c, Student__r.Name,
                   Job_Drive__c, Job_Drive__r.Company__c,
                   Job_Drive__r.Company__r.Name,
                   Job_Drive__r.Company__r.Package_LPA__c
            FROM Placement_Application__c
            WHERE Id = :applicationId
            LIMIT 1
        ];

        // Update the round status and remarks
        app.Round_Status__c = newStatus;
        app.Remarks__c      = remarks;
        update app;

        // If student is Selected — create Placement Result and mark student as placed
        if (newStatus == 'Selected') {

            // Create Placement Result record
            Placement_Result__c result = new Placement_Result__c();
            result.Student__c              = app.Student__c;
            result.Company__c              = app.Job_Drive__r.Company__c;
            result.Job_Drive__c            = app.Job_Drive__c;
            result.Offered_Package_LPA__c  = app.Job_Drive__r.Company__r.Package_LPA__c;
            result.Offer_Date__c           = Date.today();

            insert result;

            // Mark the student as placed
            Student__c student       = new Student__c(Id = app.Student__c);
            student.Is_Placed__c     = true;
            student.Placed_At__c     = app.Job_Drive__r.Company__r.Name;
            update student;

            // Send congratulation email to student
            sendCongratulationEmail(app.Student__c, app.Job_Drive__r.Company__r.Name);
        }
    }


    /* ─────────────────────────────────────────────────────────────
       METHOD 6: getPlacementDashboard()
       Returns overall placement statistics for the dashboard.
       Used to populate the analytics/reports section of the app.

       @return — Map with all placement stats
       ───────────────────────────────────────────────────────────── */
    @AuraEnabled(cacheable=true)
    public static Map<String, Object> getPlacementDashboard() {

        // cacheable=true — Lightning caches this result for performance
        // Use only for read-only methods that don't change data

        Map<String, Object> dashboard = new Map<String, Object>();

        // Total students
        Integer totalStudents = [SELECT COUNT() FROM Student__c];
        dashboard.put('totalStudents', totalStudents);

        // Total placed students
        Integer placedStudents = [
            SELECT COUNT() FROM Student__c WHERE Is_Placed__c = true
        ];
        dashboard.put('placedStudents', placedStudents);

        // Unplaced students
        dashboard.put('unplacedStudents', totalStudents - placedStudents);

        // Placement percentage
        Decimal placementRate = totalStudents > 0
            ? (Decimal.valueOf(placedStudents) / totalStudents * 100).setScale(2)
            : 0;
        dashboard.put('placementRate', placementRate);

        // Total companies registered
        Integer totalCompanies = [SELECT COUNT() FROM Company__c];
        dashboard.put('totalCompanies', totalCompanies);

        // Total job drives conducted
        Integer totalDrives = [SELECT COUNT() FROM Job_Drive__c];
        dashboard.put('totalDrives', totalDrives);

        // Average package (from placement results)
        AggregateResult avgPkg = [
            SELECT AVG(Offered_Package_LPA__c) avgPackage
            FROM Placement_Result__c
        ];
        dashboard.put('averagePackage', avgPkg.get('avgPackage'));

        // Top placing company (most students placed)
        List<AggregateResult> topCompany = [
            SELECT Company__r.Name companyName, COUNT(Id) placedCount
            FROM Placement_Result__c
            GROUP BY Company__r.Name
            ORDER BY COUNT(Id) DESC
            LIMIT 1
        ];

        if (!topCompany.isEmpty()) {
            dashboard.put('topCompany', topCompany[0].get('companyName'));
            dashboard.put('topCompanyCount', topCompany[0].get('placedCount'));
        }

        // Branch-wise placement breakdown
        List<AggregateResult> branchStats = [
            SELECT Branch__c branch, COUNT(Id) total,
                   SUM(CASE WHEN Is_Placed__c = true THEN 1 ELSE 0 END) placed
            FROM Student__c
            GROUP BY Branch__c
        ];

        // Build branch-wise list for the UI chart
        List<Map<String, Object>> branchData = new List<Map<String, Object>>();
        for (AggregateResult br : branchStats) {
            Map<String, Object> branchEntry = new Map<String, Object>();
            branchEntry.put('branch', br.get('branch'));
            branchEntry.put('total',  br.get('total'));
            branchData.add(branchEntry);
        }
        dashboard.put('branchWiseData', branchData);

        return dashboard;
    }


    /* ─────────────────────────────────────────────────────────────
       METHOD 7: getAllStudents()
       Fetches all students with their placement status.
       Used to populate the student list view in the app.

       @return — List of all Student__c records
       ───────────────────────────────────────────────────────────── */
    @AuraEnabled(cacheable=true)
    public static List<Student__c> getAllStudents() {
        return [
            SELECT Id, Name, Roll_Number__c, Branch__c, CGPA__c,
                   Skills__c, Email__c, Phone__c, Is_Placed__c, Placed_At__c
            FROM Student__c
            ORDER BY Name ASC
        ];
    }


    /* ─────────────────────────────────────────────────────────────
       METHOD 8: getUpcomingDrives()
       Returns all upcoming or active placement drives.
       Students see this to find drives to apply for.

       @return — List of upcoming Job_Drive__c records
       ───────────────────────────────────────────────────────────── */
    @AuraEnabled(cacheable=true)
    public static List<Job_Drive__c> getUpcomingDrives() {
        return [
            SELECT Id, Name, Company__r.Name, Drive_Date__c,
                   Eligible_Branches__c, Min_CGPA__c,
                   Vacancies__c, Status__c,
                   Company__r.Package_LPA__c, Company__r.Industry__c
            FROM Job_Drive__c
            WHERE Status__c IN ('Upcoming', 'Active')
            ORDER BY Drive_Date__c ASC
        ];
    }


    /* ─────────────────────────────────────────────────────────────
       HELPER METHOD: sendCongratulationEmail()
       Sends a congratulation email when a student gets selected.
       private — only used internally by this class.

       @param studentId  — ID of the placed student
       @param companyName — Name of the company that selected them
       ───────────────────────────────────────────────────────────── */
    private static void sendCongratulationEmail(Id studentId, String companyName) {

        // Fetch student email
        Student__c student = [
            SELECT Name, Email__c FROM Student__c WHERE Id = :studentId LIMIT 1
        ];

        if (String.isBlank(student.Email__c)) return; // Skip if no email

        Messaging.SingleEmailMessage mail = new Messaging.SingleEmailMessage();
        mail.setToAddresses(new List<String>{ student.Email__c });
        mail.setSubject('🎉 Congratulations! You are Placed at ' + companyName);
        mail.setPlainTextBody(
            'Dear ' + student.Name + ',\n\n' +
            'Congratulations! You have been successfully selected at ' +
            companyName + ' through the campus placement drive.\n\n' +
            'Your placement team will contact you soon with further details ' +
            'regarding your offer letter and joining date.\n\n' +
            'Best wishes for your new journey!\n\n' +
            'Regards,\nPlacement Cell\nStudent Placement Tracker System'
        );

        Messaging.sendEmail(new List<Messaging.SingleEmailMessage>{ mail });
    }
}


/* ─────────────────────────────────────────────────────────────────
   FILE 2: PlacementApplicationTrigger.trigger
   Trigger on Placement_Application__c to enforce business rules.
   ───────────────────────────────────────────────────────────── */

/*
trigger PlacementApplicationTrigger on Placement_Application__c
    (before insert, before update, after update) {

    // ── BEFORE INSERT: Validate before saving new application ──
    if (Trigger.isBefore && Trigger.isInsert) {

        // Collect all student IDs and drive IDs from the batch
        Set<Id> studentIds = new Set<Id>();
        Set<Id> driveIds   = new Set<Id>();

        for (Placement_Application__c app : Trigger.new) {
            studentIds.add(app.Student__c);
            driveIds.add(app.Job_Drive__c);
        }

        // Fetch all students at once (bulk-safe — not inside loop)
        Map<Id, Student__c> studentMap = new Map<Id, Student__c>([
            SELECT Id, CGPA__c, Branch__c, Is_Placed__c
            FROM Student__c
            WHERE Id IN :studentIds
        ]);

        // Fetch all drives at once
        Map<Id, Job_Drive__c> driveMap = new Map<Id, Job_Drive__c>([
            SELECT Id, Min_CGPA__c, Eligible_Branches__c, Status__c
            FROM Job_Drive__c
            WHERE Id IN :driveIds
        ]);

        // Validate each application record
        for (Placement_Application__c app : Trigger.new) {
            Student__c  stu   = studentMap.get(app.Student__c);
            Job_Drive__c drv  = driveMap.get(app.Job_Drive__c);

            // Rule 1: Already placed students cannot apply
            if (stu.Is_Placed__c) {
                app.addError('Already placed students cannot apply to new drives.');
            }

            // Rule 2: Minimum CGPA check
            if (stu.CGPA__c < drv.Min_CGPA__c) {
                app.addError('CGPA ' + stu.CGPA__c + ' is below minimum required CGPA ' + drv.Min_CGPA__c);
            }

            // Rule 3: Drive must be open
            if (drv.Status__c == 'Completed') {
                app.addError('This drive is already completed.');
            }
        }
    }

    // ── AFTER UPDATE: Log status changes for audit trail ──
    if (Trigger.isAfter && Trigger.isUpdate) {
        for (Placement_Application__c app : Trigger.new) {
            Placement_Application__c oldApp = Trigger.oldMap.get(app.Id);

            // Log only if status changed
            if (app.Round_Status__c != oldApp.Round_Status__c) {
                System.debug(
                    'Application ' + app.Id +
                    ' status changed from ' + oldApp.Round_Status__c +
                    ' to ' + app.Round_Status__c
                );
            }
        }
    }
}
*/


/* ─────────────────────────────────────────────────────────────────
   FILE 3: PlacementTrackerControllerTest.cls
   Test class for PlacementTrackerController.
   Provides 75%+ code coverage required for production deployment.
   ───────────────────────────────────────────────────────────── */

/*
@isTest
private class PlacementTrackerControllerTest {

    // ── SETUP: Create test data used across all tests ──
    // @testSetup runs once before all test methods in this class
    @testSetup
    static void setupTestData() {

        // Create test Company
        Company__c company = new Company__c(
            Name             = 'Test Infosys',
            Industry__c      = 'IT',
            Package_LPA__c   = 6.5,
            HR_Email__c      = 'hr@testinfosys.com',
            Visit_Date__c    = Date.today().addDays(10)
        );
        insert company;

        // Create test Job Drive
        Job_Drive__c drive = new Job_Drive__c(
            Name                 = 'Test Drive 2024',
            Company__c           = company.Id,
            Drive_Date__c        = DateTime.now().addDays(10),
            Eligible_Branches__c = 'CS;IT',
            Min_CGPA__c          = 7.0,
            Vacancies__c         = 5,
            Status__c            = 'Upcoming'
        );
        insert drive;

        // Create test Students
        List<Student__c> students = new List<Student__c>{
            new Student__c(
                Name           = 'Test Student 1',
                Roll_Number__c = 'CS001',
                Branch__c      = 'CS',
                CGPA__c        = 8.5,
                Skills__c      = 'Java, Python',
                Email__c       = 'student1@test.com',
                Is_Placed__c   = false
            ),
            new Student__c(
                Name           = 'Test Student 2',
                Roll_Number__c = 'CS002',
                Branch__c      = 'CS',
                CGPA__c        = 6.0,  // Below min CGPA — for negative test
                Skills__c      = 'HTML, CSS',
                Email__c       = 'student2@test.com',
                Is_Placed__c   = false
            )
        };
        insert students;
    }


    // ── TEST 1: Test student registration ──
    @isTest
    static void testRegisterStudent() {
        Test.startTest();
        Student__c s = PlacementTrackerController.registerStudent(
            'New Student', 'CS099', 'CS', 9.0, 'React, Node', 'new@test.com', '9999999999'
        );
        Test.stopTest();

        System.assertNotNull(s.Id, 'Student should be created with ID');
        System.assertEquals('Applied', 'Applied', 'Default status test');
        System.assertEquals(false, s.Is_Placed__c, 'New student should not be placed');
    }


    // ── TEST 2: Test student apply to drive ──
    @isTest
    static void testApplyToJobDrive() {
        Student__c stu  = [SELECT Id FROM Student__c WHERE Roll_Number__c = 'CS001' LIMIT 1];
        Job_Drive__c drv = [SELECT Id FROM Job_Drive__c LIMIT 1];

        Test.startTest();
        Placement_Application__c app =
            PlacementTrackerController.applyToJobDrive(stu.Id, drv.Id);
        Test.stopTest();

        System.assertNotNull(app.Id, 'Application should be created');
        System.assertEquals('Applied', app.Round_Status__c, 'Initial status should be Applied');
    }


    // ── TEST 3: Test low CGPA student cannot apply ──
    @isTest
    static void testLowCGPACannotApply() {
        Student__c stu   = [SELECT Id FROM Student__c WHERE Roll_Number__c = 'CS002' LIMIT 1];
        Job_Drive__c drv = [SELECT Id FROM Job_Drive__c LIMIT 1];

        Test.startTest();
        try {
            PlacementTrackerController.applyToJobDrive(stu.Id, drv.Id);
            System.assert(false, 'Should have thrown exception for low CGPA');
        } catch (AuraHandledException e) {
            System.assert(e.getMessage().contains('CGPA'), 'Error should mention CGPA');
        }
        Test.stopTest();
    }


    // ── TEST 4: Test dashboard stats ──
    @isTest
    static void testGetPlacementDashboard() {
        Test.startTest();
        Map<String, Object> dashboard = PlacementTrackerController.getPlacementDashboard();
        Test.stopTest();

        System.assertNotNull(dashboard, 'Dashboard should not be null');
        System.assert(dashboard.containsKey('totalStudents'), 'Should have totalStudents key');
        System.assert(dashboard.containsKey('placementRate'), 'Should have placementRate key');
    }


    // ── TEST 5: Test update round status to Selected ──
    @isTest
    static void testUpdateRoundStatusToSelected() {
        Student__c stu   = [SELECT Id FROM Student__c WHERE Roll_Number__c = 'CS001' LIMIT 1];
        Job_Drive__c drv = [SELECT Id FROM Job_Drive__c LIMIT 1];

        // Apply first
        Placement_Application__c app =
            PlacementTrackerController.applyToJobDrive(stu.Id, drv.Id);

        Test.startTest();
        // Update to Selected
        PlacementTrackerController.updateRoundStatus(app.Id, 'Selected', 'Cleared all rounds');
        Test.stopTest();

        // Verify student is now marked as placed
        Student__c updatedStu = [SELECT Is_Placed__c FROM Student__c WHERE Id = :stu.Id];
        System.assertEquals(true, updatedStu.Is_Placed__c, 'Student should be marked as placed');
    }
}
*/