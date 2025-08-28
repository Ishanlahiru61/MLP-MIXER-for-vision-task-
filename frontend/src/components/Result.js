import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import ResultBox from "./ResultBox";

export default function Result() {
  const location = useLocation();
  const navigate = useNavigate();
  const predictionData = location.state?.predictionData;

  if (!predictionData) {
    return (
      <div className="text-center mt-20">
        <p>No prediction data found.</p>
        <button
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
          onClick={() => navigate("/")}
        >
          Go Back
        </button>
      </div>
    );
  }

  return (
    <div>
      <ResultBox predictionData={predictionData} />
      <div className="flex justify-center mt-4">
        <button
          className="px-4 py-2 bg-blue-500 text-white rounded"
          onClick={() => navigate("/")}
        >
          Predict Another
        </button>
      </div>
    </div>
  );
}
