import React from "react";

export default function ResultBox({ predictionData }) {
  if (!predictionData) return null;

  const { predictedClass, confidence, accuracy, imageUrl } = predictionData;

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-100 to-purple-100 p-6">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-96 flex flex-col items-center transition-transform transform hover:scale-105">
        <h2 className="text-3xl font-extrabold text-gray-800 mb-6">Prediction Result</h2>

        {imageUrl && (
          <img
            src={imageUrl}
            alt="Uploaded"
            className="w-64 h-64 object-cover rounded-xl shadow-md mb-6"
          />
        )}

        <p className="text-xl font-semibold text-gray-700 mb-2">
          Class: <span className="text-blue-600">{predictedClass}</span>
        </p>

        <p className="text-xl font-semibold text-gray-700 mb-2">
          Confidence: <span className="text-green-500">{(confidence * 100).toFixed(2)}%</span>
        </p>

        <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
          <div
            className="bg-green-500 h-4 rounded-full transition-all duration-700"
            style={{ width: `${(confidence * 100).toFixed(2)}%` }}
          />
        </div>

        <p className="text-lg font-medium text-gray-600">
          Model Accuracy: <span className="text-purple-600">{(accuracy * 100).toFixed(2)}%</span>
        </p>
      </div>
    </div>
  );
}
