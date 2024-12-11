import React from "react";
import { Card, CardContent, Typography, Box } from "@mui/material";
import { useNavigate } from "react-router-dom";

const TestCard = ({ test }) => {
  const navigate = useNavigate();

  const handleCardClick = () => {
    navigate(`/testinstructions/${test.contest_id}`);
  };

  return (
    <Card
      variant="outlined"
      style={{
        borderRadius: "10px",
        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
        marginBottom: "16px",
        cursor: "pointer",
      }}
      onClick={handleCardClick}
    >
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6" style={{ fontWeight: "bold", color: "#1E293B" }}>
            {test.contest_name}
          </Typography>
          <Box display="flex" alignItems="center">
            <Typography variant="body2" style={{ color: "#6B7280" }}>
              Open
            </Typography>
            <span style={{ color: "#10B981", fontSize: "2rem", marginLeft: "4px" }}>•</span>
          </Box>
        </Box>
        <Typography variant="body2" style={{ color: "#374151", marginTop: "8px" }}>
          Organization: {test.organization_name} ({test.organization_type})
        </Typography>
        <Typography
          variant="body2"
          style={{ color: "#4B5563", marginTop: "4px", fontStyle: "italic" }}
        >
          {new Date(test.start_time).toLocaleString()} -{" "}
          {new Date(test.end_time).toLocaleString()}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default TestCard;
