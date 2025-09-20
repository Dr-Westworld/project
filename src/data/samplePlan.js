// Sample plan data structure for demonstration
export const samplePlan = {
  planId: "plan_123456789",
  taskTitle: "Register Private Limited Company in California",
  status: "ready",
  description: "Complete step-by-step guide to register your LLC in California based on your uploaded documents",
  jurisdiction: "California, USA",
  documentType: "incorporation",
  stages: [
    {
      id: "stage_1",
      title: "Create Government Account",
      shortDescription: "Register on the official government portal",
      isCompleted: false,
      stageNumber: 1,
      estimatedTime: "30 minutes",
      requiredDocuments: ["Government ID", "Email Address"],
      responsibleParty: "user",
      confidence: "high",
      website: "https://bizfileonline.sos.ca.gov/",
      citations: [
        {
          url: "https://bizfileonline.sos.ca.gov/",
          title: "California Secretary of State - BizFile Online",
          source_type: "government",
          excerpt: "Official portal for business filings in California",
          date: "2024-01-15"
        }
      ],
      subStages: [
        {
          id: "stage_1_1",
          title: "Visit Registration Page",
          shortDescription: "Navigate to the registration page",
          isCompleted: false,
          stageNumber: 1,
          estimatedTime: "5 minutes",
          responsibleParty: "user",
          confidence: "high",
          website: "https://bizfileonline.sos.ca.gov/",
          subStages: [
            {
              id: "stage_1_1_1",
              title: "Open Browser",
              shortDescription: "Open your web browser",
              isCompleted: false,
              stageNumber: 1,
              estimatedTime: "1 minute",
              responsibleParty: "user",
              confidence: "high"
            },
            {
              id: "stage_1_1_2",
              title: "Navigate to URL",
              shortDescription: "Type or paste the government portal URL",
              isCompleted: false,
              stageNumber: 2,
              estimatedTime: "2 minutes",
              responsibleParty: "user",
              confidence: "high",
              website: "https://bizfileonline.sos.ca.gov/"
            }
          ]
        },
        {
          id: "stage_1_2",
          title: "Fill Personal Information",
          shortDescription: "Enter your personal details in the registration form",
          isCompleted: false,
          stageNumber: 2,
          estimatedTime: "10 minutes",
          requiredDocuments: ["Government ID", "Address Proof"],
          responsibleParty: "user",
          confidence: "high",
          warnings: ["Ensure all information matches your government ID"],
          subStages: [
            {
              id: "stage_1_2_1",
              title: "Enter Full Name",
              shortDescription: "Enter your legal name as it appears on ID",
              isCompleted: false,
              stageNumber: 1,
              estimatedTime: "2 minutes",
              responsibleParty: "user",
              confidence: "high"
            },
            {
              id: "stage_1_2_2",
              title: "Enter Contact Information",
              shortDescription: "Provide email and phone number",
              isCompleted: false,
              stageNumber: 2,
              estimatedTime: "3 minutes",
              responsibleParty: "user",
              confidence: "high"
            },
            {
              id: "stage_1_2_3",
              title: "Enter Address",
              shortDescription: "Provide your business address",
              isCompleted: false,
              stageNumber: 3,
              estimatedTime: "5 minutes",
              requiredDocuments: ["Address Proof"],
              responsibleParty: "user",
              confidence: "high"
            }
          ]
        },
        {
          id: "stage_1_3",
          title: "Verify Email Address",
          shortDescription: "Click verification link sent to your email",
          isCompleted: false,
          stageNumber: 3,
          estimatedTime: "5 minutes",
          responsibleParty: "user",
          confidence: "high",
          warnings: ["Check spam folder if email doesn't arrive within 5 minutes"]
        }
      ],
      createdAt: "2024-01-15T10:00:00Z",
      updatedAt: "2024-01-15T10:00:00Z"
    },
    {
      id: "stage_2",
      title: "Prepare Required Documents",
      shortDescription: "Gather all necessary documentation for LLC formation",
      isCompleted: false,
      stageNumber: 2,
      estimatedTime: "2-3 hours",
      requiredDocuments: [
        "Articles of Organization",
        "Operating Agreement",
        "Statement of Information",
        "Registered Agent Information"
      ],
      responsibleParty: "user",
      confidence: "medium",
      citations: [
        {
          url: "https://sos.ca.gov/business/llc/",
          title: "California LLC Requirements",
          source_type: "government",
          excerpt: "Required documents for LLC formation in California",
          date: "2024-01-10"
        },
        {
          url: "https://www.ftb.ca.gov/forms/2019/2019-3520.pdf",
          title: "California Form 3520 - LLC Return",
          source_type: "government",
          excerpt: "Tax form required for LLCs",
          date: "2024-01-05"
        }
      ],
      warnings: [
        "Ensure all documents are notarized",
        "Check for any state-specific requirements",
        "Keep copies of all documents"
      ],
      subStages: [
        {
          id: "stage_2_1",
          title: "Draft Articles of Organization",
          shortDescription: "Create the Articles of Organization document",
          isCompleted: false,
          stageNumber: 1,
          estimatedTime: "1 hour",
          requiredDocuments: ["Company Name", "Business Address", "Registered Agent Info"],
          responsibleParty: "user",
          confidence: "medium",
          website: "https://sos.ca.gov/business/llc/",
          subStages: [
            {
              id: "stage_2_1_1",
              title: "Choose Company Name",
              shortDescription: "Select a unique company name",
              isCompleted: false,
              stageNumber: 1,
              estimatedTime: "30 minutes",
              responsibleParty: "user",
              confidence: "high",
              warnings: ["Name must be unique and include LLC designation"]
            },
            {
              id: "stage_2_1_2",
              title: "Fill Articles Template",
              shortDescription: "Complete the Articles of Organization form",
              isCompleted: false,
              stageNumber: 2,
              estimatedTime: "30 minutes",
              requiredDocuments: ["Articles Template"],
              responsibleParty: "user",
              confidence: "high"
            }
          ]
        },
        {
          id: "stage_2_2",
          title: "Create Operating Agreement",
          shortDescription: "Draft the LLC Operating Agreement",
          isCompleted: false,
          stageNumber: 2,
          estimatedTime: "1-2 hours",
          requiredDocuments: ["Operating Agreement Template"],
          responsibleParty: "user",
          confidence: "low",
          warnings: ["Consider consulting a lawyer for complex agreements"]
        },
        {
          id: "stage_2_3",
          title: "Prepare Statement of Information",
          shortDescription: "Complete the Statement of Information form",
          isCompleted: false,
          stageNumber: 3,
          estimatedTime: "30 minutes",
          requiredDocuments: ["Statement of Information Form"],
          responsibleParty: "user",
          confidence: "high"
        }
      ],
      createdAt: "2024-01-15T10:00:00Z",
      updatedAt: "2024-01-15T10:00:00Z"
    },
    {
      id: "stage_3",
      title: "Submit Application",
      shortDescription: "File the incorporation documents with the state",
      isCompleted: false,
      stageNumber: 3,
      estimatedTime: "1 hour",
      requiredDocuments: ["Completed Application", "Filing Fee"],
      responsibleParty: "user",
      confidence: "high",
      website: "https://bizfileonline.sos.ca.gov/",
      dependencies: ["stage_1", "stage_2"],
      citations: [
        {
          url: "https://bizfileonline.sos.ca.gov/",
          title: "BizFile Online Filing System",
          source_type: "government",
          excerpt: "Online system for filing business documents",
          date: "2024-01-15"
        }
      ],
      subStages: [
        {
          id: "stage_3_1",
          title: "Upload Documents",
          shortDescription: "Upload all required documents to the portal",
          isCompleted: false,
          stageNumber: 1,
          estimatedTime: "30 minutes",
          requiredDocuments: ["Articles of Organization", "Operating Agreement"],
          responsibleParty: "user",
          confidence: "high"
        },
        {
          id: "stage_3_2",
          title: "Pay Filing Fees",
          shortDescription: "Complete payment for state filing fees",
          isCompleted: false,
          stageNumber: 2,
          estimatedTime: "15 minutes",
          requiredDocuments: ["Payment Method"],
          responsibleParty: "user",
          confidence: "high"
        },
        {
          id: "stage_3_3",
          title: "Submit Application",
          shortDescription: "Final submission of the complete application",
          isCompleted: false,
          stageNumber: 3,
          estimatedTime: "15 minutes",
          responsibleParty: "user",
          confidence: "high"
        }
      ],
      createdAt: "2024-01-15T10:00:00Z",
      updatedAt: "2024-01-15T10:00:00Z"
    },
    {
      id: "stage_4",
      title: "Obtain Business Licenses",
      shortDescription: "Apply for necessary business licenses and permits",
      isCompleted: false,
      stageNumber: 4,
      estimatedTime: "2-4 weeks",
      requiredDocuments: ["LLC Certificate", "Business License Application"],
      responsibleParty: "user",
      confidence: "medium",
      dependencies: ["stage_3"],
      citations: [
        {
          url: "https://www.cdtfa.ca.gov/",
          title: "California Department of Tax and Fee Administration",
          source_type: "government",
          excerpt: "Information about business licenses and permits",
          date: "2024-01-12"
        }
      ],
      warnings: [
        "Processing time varies by jurisdiction",
        "Some licenses may require additional documentation"
      ],
      subStages: [
        {
          id: "stage_4_1",
          title: "Research Required Licenses",
          shortDescription: "Determine which licenses your business needs",
          isCompleted: false,
          stageNumber: 1,
          estimatedTime: "1 hour",
          responsibleParty: "user",
          confidence: "medium"
        },
        {
          id: "stage_4_2",
          title: "Apply for State Licenses",
          shortDescription: "Submit applications for state-level licenses",
          isCompleted: false,
          stageNumber: 2,
          estimatedTime: "2 hours",
          requiredDocuments: ["License Applications"],
          responsibleParty: "user",
          confidence: "medium"
        },
        {
          id: "stage_4_3",
          title: "Apply for Local Licenses",
          shortDescription: "Submit applications for local business licenses",
          isCompleted: false,
          stageNumber: 3,
          estimatedTime: "1 hour",
          requiredDocuments: ["Local License Applications"],
          responsibleParty: "user",
          confidence: "medium"
        }
      ],
      createdAt: "2024-01-15T10:00:00Z",
      updatedAt: "2024-01-15T10:00:00Z"
    }
  ],
  metadata: {
    totalStages: 4,
    completedStages: 0,
    estimatedTotalTime: "3-5 weeks",
    confidence: "high"
  },
  createdAt: "2024-01-15T10:00:00Z",
  updatedAt: "2024-01-15T10:00:00Z"
};

export default samplePlan;
