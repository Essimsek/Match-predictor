import { useState, useEffect } from "react";
import { FixturesType } from "./FixturesList";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./ui/card";
import { Button } from "./ui/button";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import {
  ChartContainer,
  ChartTooltipContent,
} from "./ui/chart";
import api from "../api/api";

interface PredictionData {
    away_team: string;
    home_team: string;
    predicted_outcome: string;
    probabilities: {
        away_win: number;
        draw: number;
        home_win: number;
    };
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28'];

function FixtureCard({ fixture }: { fixture: FixturesType }) {
  const [showPrediction, setShowPrediction] = useState(false);
  const [prediction, setPrediction] = useState<PredictionData | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!showPrediction) {
      setPrediction(null);
    }
  }, [showPrediction]);

  const fetchPrediction = async () => {
    if (showPrediction) {
      setShowPrediction(false);
      return;
    }

    setLoading(true);
    try {
      const response = await api.get<PredictionData>("/predict", {
        params: { home: fixture.home, away: fixture.away },
      });
      const data = response.data;
      setPrediction(data);
      setShowPrediction(true);
    } catch (error) {
      console.error("Failed to fetch prediction:", error);
    } finally {
      setLoading(false);
    }
  };

  const predictionData = prediction
    ? [
        { outcome: "Home Win", probability: prediction.probabilities.home_win * 100 },
        { outcome: "Draw", probability: prediction.probabilities.draw * 100 },
        { outcome: "Away Win", probability: prediction.probabilities.away_win * 100 },
      ]
    : [];

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">Match Prediction</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <img
              src={fixture.home_logo}
              alt={fixture.home}
              className="w-8 h-8"
            />
            <span className="font-semibold">{fixture.home}</span>
          </div>

          <div className="text-center">
            <p className="text-sm text-gray-500">{fixture.status}</p>
            <p className="text-lg font-bold">{fixture.value}</p>
          </div>

          <div className="flex items-center gap-2">
            <span className="font-semibold">{fixture.away}</span>
            <img
              src={fixture.away_logo}
              alt={fixture.away}
              className="w-8 h-8"
            />
          </div>
        </div>

        {showPrediction && prediction && (
          <div className="mt-4">
            <ChartContainer config={{}}>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={predictionData}>
                  <XAxis dataKey="outcome" />
                  <YAxis />
                  <Tooltip content={<ChartTooltipContent />} />
                  <Bar dataKey="probability">
                    {predictionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </ChartContainer>
            <div className="text-center text-sm text-muted-foreground mt-2">
              Prediction Probabilities
            </div>
          </div>
        )}
      </CardContent>
      <CardFooter>
        <Button
          onClick={fetchPrediction}
          disabled={loading}
          className="w-full"
          variant={showPrediction ? "outline" : "default"}
        >
          {loading
            ? "Predicting..."
            : showPrediction
            ? "Hide Prediction"
            : "Predict Result"}
        </Button>
      </CardFooter>
    </Card>
  );
}

export default FixtureCard;