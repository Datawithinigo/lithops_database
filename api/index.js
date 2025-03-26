export default function handler(req, res) {
  res.status(200).json({
    name: "GreenComputingLithops API",
    description: "API for accessing Intel processor data with a focus on power consumption metrics",
    version: "1.0.0",
    endpoints: [
      {
        path: "/api/processors",
        method: "GET",
        description: "Get all processors with pagination",
        parameters: {
          skip: "Number of records to skip (default: 0)",
          limit: "Number of records to return (default: 100)"
        }
      },
      {
        path: "/api/processors/[id]",
        method: "GET",
        description: "Get a processor by ID",
        parameters: {
          id: "The ID of the processor"
        }
      },
      {
        path: "/api/processor/tdp/[name]",
        method: "GET",
        description: "Get TDP information for a processor by name",
        parameters: {
          name: "The name of the processor"
        }
      },
      {
        path: "/api/upload-csv",
        method: "POST",
        description: "Upload processor data via CSV",
        body: "CSV content with processor data"
      },
      {
        path: "/api/setup-db",
        method: "GET",
        description: "Set up the database schema"
      }
    ],
    project: "https://github.com/yourusername/GreenComputingLithops",
    documentation: "https://github.com/yourusername/GreenComputingLithops#readme"
  });
}
