"use client";

import axios from "axios";

import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Label,
  LabelList,
  Line,
  LineChart,
  PolarAngleAxis,
  RadialBar,
  RadialBarChart,
  Rectangle,
  ReferenceLine,
  XAxis,
  YAxis,
} from "recharts";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components//ui/card";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components//ui/chart";
import { Separator } from "@/components//ui/separator";
import { useEffect, useState } from "react";

export const description = "A collection of health charts.";

export const chartData = [
  { month: "Cloud", desktop: 186, mobile: 80 },
  { month: "Storage", desktop: 305, mobile: 200 },
  { month: "Distribution", desktop: 237, mobile: 120 },
];

export const chartConfig = {
  desktop: {
    label: "original",
    color: "hsl(var(--chart-1))",
  },
  mobile: {
    label: "new",
    color: "hsl(var(--chart-2))",
  },
};

function USimpleBlock(props) {
  return (
    <Card className="max-w-xs uBox1" x-chunk="charts-01-chunk-7">
      <CardHeader className="space-y-0 pb-0">
        <CardDescription>{props.featureName}</CardDescription>
        <CardTitle className="flex items-baseline gap-1 text-4xl tabular-nums">
          {props.value}
        </CardTitle>
      </CardHeader>
      <CardContent className="p-0"></CardContent>
    </Card>
  );
}

function UAiAssistant(props) {
  return (
    <Card className="max-w-xs uBox1">
      <CardHeader>
        <CardTitle>{props.title}</CardTitle>
      </CardHeader>
      <CardContent className="gap-1">{props.description}</CardContent>
    </Card>
  );
}

function USummaryBlock(props) {
  return (
    <Card className="max-w-xs uBox1" x-chunk="charts-01-chunk-7">
      <CardHeader>
        <CardTitle>{props.title}</CardTitle>
      </CardHeader>
      <CardContent className="gap-1">{props.description}</CardContent>
    </Card>
  );
}

function UTrafficCostBlock(props) {
  return (
    <Card className="max-w-xs uBox1" x-chunk="charts-01-chunk-7">
      <CardHeader>
        <CardTitle>{props.title}</CardTitle>
      </CardHeader>
      <CardContent className="gap-1">
        <ChartContainer config={chartConfig}>
          <LineChart
            accessibilityLayer
            data={chartData}
            margin={{
              left: 12,
              right: 12,
            }}
          >
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="month"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              tickFormatter={(value) => value.slice(0, 3)}
            />
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent hideLabel />}
            />
            <Line
              dataKey="desktop"
              type="natural"
              stroke="var(--color-desktop)"
              strokeWidth={2}
              dot={{
                fill: "var(--color-desktop)",
              }}
              activeDot={{
                r: 6,
              }}
            />
          </LineChart>
        </ChartContainer>
      </CardContent>
    </Card>
  );
}

export default function Charts() {
  const [monthlyCost, setMonthlyCost] = useState("");
  const [estimatedSavings, setEstimatedSavings] = useState("");
  const [serverUptime, setServerUptime] = useState("");
  const [currentTraffic, setCurrentTraffic] = useState("");
  const [summary, setSummary] = useState("");
  const [aiAssistantResp, setAiAssistantResp] = useState("");
  const [costComparisonData, setCostComparisonData] = useState({});
  const [revenueComparisonData, setRevenueComparisonData] = useState({});
  const [trafficComparisonData, setTrafficComparisonData] = useState({});

  useEffect(() => {
    axios.get("http://localhost:8000/api/current_state").then((res) => {
      console.log(res);
      setMonthlyCost(res.data.content.currentMonthlyCost.value);
      setEstimatedSavings(res.data.content.estimatedSavings.value);
      setServerUptime(res.data.content.serverUptime.value);
      setCurrentTraffic(res.data.content.currentTraffic.value);
      setSummary(res.data.content.summary.value);
      setAiAssistantResp(res.data.content.aiAssistantResp.value);
      setCostComparisonData(res.data.content.costComparison);
      // setRevenueComparisonData(res.data.content.revenueComparison);

      // console.log(`"costComparisonData: ${costComparisonData}`);

      function sleep(time) {
        return new Promise((resolve) => setTimeout(resolve, time));
      }

      sleep(10000);

      // console.log(costComparisonData);
    });
    console.log("testing integration. ");
  }, []);

  function URevenueComparisionBlock(props) {
    return (
      <Card className="max-w-xs uBox1" x-chunk="charts-01-chunk-7">
        <CardHeader>
          <CardTitle>{props.title}</CardTitle>
        </CardHeader>
        <CardContent className="gap-1">
          <ChartContainer config={chartConfig}>
            <AreaChart
              accessibilityLayer
              data={chartData}
              margin={{
                left: 12,
                right: 12,
              }}
            >
              <CartesianGrid vertical={false} />
              <XAxis
                dataKey="month"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                tickFormatter={(value) => value.slice(0, 3)}
              />
              <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
              <defs>
                <linearGradient id="fillDesktop" x1="0" y1="0" x2="0" y2="1">
                  <stop
                    offset="5%"
                    stopColor="var(--color-desktop)"
                    stopOpacity={0.8}
                  />
                  <stop
                    offset="95%"
                    stopColor="var(--color-desktop)"
                    stopOpacity={0.1}
                  />
                </linearGradient>
                <linearGradient id="fillMobile" x1="0" y1="0" x2="0" y2="1">
                  <stop
                    offset="5%"
                    stopColor="var(--color-mobile)"
                    stopOpacity={0.8}
                  />
                  <stop
                    offset="95%"
                    stopColor="var(--color-mobile)"
                    stopOpacity={0.1}
                  />
                </linearGradient>
              </defs>
              <Area
                dataKey="mobile"
                type="natural"
                fill="url(#fillMobile)"
                fillOpacity={0.4}
                stroke="var(--color-mobile)"
                stackId="a"
              />
              <Area
                dataKey="desktop"
                type="natural"
                fill="url(#fillDesktop)"
                fillOpacity={0.4}
                stroke="var(--color-desktop)"
                stackId="a"
              />
            </AreaChart>
          </ChartContainer>
        </CardContent>
      </Card>
    );
  }

  function UCostComparisionBlock(props) {
    // console.log(props.costComparisonData);
    console.log(props);
    return (
      <Card className="max-w-xs uBox1" x-chunk="charts-01-chunk-7">
        <CardHeader>
          <CardTitle>{props.title}</CardTitle>
        </CardHeader>
        <CardContent className="gap-1">
          <ChartContainer config={chartConfig}>
            <BarChart accessibilityLayer data={costComparisonData}>
              <CartesianGrid vertical={false} />
              <XAxis
                dataKey="label"
                tickLine={false}
                tickMargin={10}
                axisLine={false}
                tickFormatter={(value) => value.slice(0, 3)}
              />
              <ChartTooltip
                cursor={false}
                content={<ChartTooltipContent indicator="dashed" />}
              />
              <Bar dataKey="original" fill="var(--color-desktop)" radius={4} />
              <Bar dataKey="new" fill="var(--color-mobile)" radius={4} />
            </BarChart>
          </ChartContainer>
        </CardContent>
      </Card>
    );
  }

  return (
    <main>
      <div className="chart-wrapper mx-auto flex max-w-6xl flex-col flex-wrap items-start justify-center gap-6 p-6 sm:flex-row">
        <p className="text-xl font-bold">Tech Stack Optimization Dashboard</p>
      </div>

      <div className="chart-wrapper mx-auto flex max-w-6xl flex-col flex-wrap items-start justify-center gap-6 p-6 sm:flex-row sm:p-8">
        <div className="grid w-full flex-1 gap-6">
          <USimpleBlock
            value={monthlyCost}
            featureName={"Current Monthly Cost"}
          />
          <UAiAssistant title={"AI Assistant"} description={aiAssistantResp} />
        </div>
        <div className="grid w-full flex-1 gap-6">
          <USimpleBlock
            value={estimatedSavings}
            featureName={"Estimated Savings"}
          />
          <USummaryBlock title={"Summary"} description={summary} />
          <UCostComparisionBlock
            title={"Cost Comparison"}
            chartData={costComparisonData}
          />
        </div>
        <div className="grid w-full flex-1 gap-6">
          <USimpleBlock value={serverUptime} featureName={"Server Uptime"} />
          <URevenueComparisionBlock title={"[TODO] Comparison of Revenue"} />
        </div>
        <div className="grid w-full flex-1 gap-6">
          <USimpleBlock
            value={currentTraffic}
            featureName={"Current Traffic"}
          />
          <UTrafficCostBlock title={"[TODO] Traffic vs Cost"} />
        </div>
      </div>
    </main>
  );
}
