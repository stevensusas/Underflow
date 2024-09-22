"use client";

import axios from "axios";

import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import { ScrollArea } from "@/components/ui/scroll-area";

import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  XAxis,
} from "recharts";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components//ui/card";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components//ui/chart";
import { useEffect, useState } from "react";

export const description = "A collection of health charts.";

// export const oldServices = [
//   { name: "S3", type: "Storage", cost: "$50.00" },
//   { name: "S3", type: "Storage", cost: "$50.00" },
// ];

export const invoices = [
  {
    invoice: "INV001",
    paymentStatus: "Paid",
    totalAmount: "$250.00",
    paymentMethod: "Credit Card",
  },
  {
    invoice: "INV002",
    paymentStatus: "Pending",
    totalAmount: "$150.00",
    paymentMethod: "PayPal",
  },
  {
    invoice: "INV003",
    paymentStatus: "Unpaid",
    totalAmount: "$350.00",
    paymentMethod: "Bank Transfer",
  },
  {
    invoice: "INV004",
    paymentStatus: "Paid",
    totalAmount: "$450.00",
    paymentMethod: "Credit Card",
  },
  {
    invoice: "INV005",
    paymentStatus: "Paid",
    totalAmount: "$550.00",
    paymentMethod: "PayPal",
  },
  {
    invoice: "INV006",
    paymentStatus: "Pending",
    totalAmount: "$200.00",
    paymentMethod: "Bank Transfer",
  },
  {
    invoice: "INV007",
    paymentStatus: "Unpaid",
    totalAmount: "$300.00",
    paymentMethod: "Credit Card",
  },
];

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
    <Card className="max-w-xs uBoxReport">
      <CardHeader>
        <CardTitle>{props.title}</CardTitle>
      </CardHeader>

      <CardContent className="gap-1">
        <ScrollArea className="h-[250px] w-full rounded-md border p-4">
          {props.description}
        </ScrollArea>
      </CardContent>
    </Card>
  );
}

function USummaryBlock(props) {
  return (
    <Card className="max-w-xs uBox1" x-chunk="charts-01-chunk-7">
      <CardHeader>
        <CardTitle>
          {/* <ChartColumn
            color="black"
            size={18}
            style={{ verticalAlign: "middle", display: "inline-block" }}
          />{" "} */}
          {props.title}
        </CardTitle>
      </CardHeader>
      <CardContent className="gap-1">{props.description}</CardContent>
    </Card>
  );
}

export default function Charts() {
  const [monthlyCost, setMonthlyCost] = useState("");
  const [newMonthlyCost, setNewMonthlyCost] = useState("");
  const [estimatedSavings, setEstimatedSavings] = useState("");
  const [serverUptime, setServerUptime] = useState("");
  const [currentTraffic, setCurrentTraffic] = useState("");
  const [summary, setSummary] = useState("");
  const [aiAssistantResp, setAiAssistantResp] = useState("");
  const [costComparisonData, setCostComparisonData] = useState(null);
  const [revenueComparisonData, setRevenueComparisonData] = useState(null);
  const [trafficComparisonData, setTrafficComparisonData] = useState({});
  const [repositoryName, setRepositoryName] = useState("");
  const [oldServices, setOldServices] = useState([]);
  const [newServices, setNewServices] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/api/current_state").then((res) => {
      console.log(res);
      setMonthlyCost(res.data.content.currentMonthlyCost.value);
      setNewMonthlyCost(res.data.content.newMonthlyCost.value);
      setEstimatedSavings(res.data.content.estimatedSavings.value);
      setServerUptime(res.data.content.serverUptime.value);
      setCurrentTraffic(res.data.content.currentTraffic.value);
      setSummary(res.data.content.summary.value);
      setAiAssistantResp(res.data.content.aiAssistantResp.value);
      setCostComparisonData(res.data.content.costComparisonV2);
      setRevenueComparisonData(res.data.content.revenueComparison);
      setTrafficComparisonData(res.data.content.trafficCostComparison);
      setRepositoryName(res.data.content.repositoryName);
      setNewServices(res.data.content.newServices);
      setOldServices(res.data.content.oldServices);

      function sleep(time) {
        return new Promise((resolve) => setTimeout(resolve, time));
      }

      sleep(10000);

      // console.log(costComparisonData);
    });
    console.log("testing integration. ");
  }, []);

  function UServiceTable(props) {
    console.log(props);
    return (
      <Card className="max-w-xs uBox1" x-chunk="charts-01-chunk-7">
        <CardHeader>
          <CardTitle>{props.title}</CardTitle>
        </CardHeader>
        <CardContent className="gap-1">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[100px]">Name</TableHead>
                <TableHead>Type</TableHead>
                <TableHead className="text-right">Cost</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {props.tabularData.map((service) => (
                <TableRow key={service.name}>
                  <TableCell className="font-medium">{service.name}</TableCell>
                  <TableCell>{service.type}</TableCell>
                  <TableCell className="text-right">{service.cost}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
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
              data={[
                { label: 0.03, new: 400000.0, original: 400000.0 },
                { label: 0.022, new: 950000.0, original: 950000.0 },
              ]}
              margin={{
                left: 12,
                right: 12,
              }}
            >
              <CartesianGrid vertical={false} />
              <XAxis
                dataKey="label"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                // tickFormatter={(value) => value.slice(0, 3)}
              />
              <ChartTooltip
                cursor={false}
                content={<ChartTooltipContent hideLabel />}
              />
              <Line
                dataKey="new"
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
              data={revenueComparisonData}
              margin={{
                left: 12,
                right: 12,
              }}
            >
              <CartesianGrid vertical={false} />
              <XAxis
                dataKey="label"
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
                dataKey="new"
                type="natural"
                fill="url(#fillMobile)"
                fillOpacity={0.4}
                stroke="var(--color-mobile)"
                stackId="a"
              />
              <Area
                dataKey="original"
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
                // tickFormatter={(value) => value.slice(0, 3)}
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

  console.log(oldServices);

  return (
    <main>
      <div className="justify-center gap-6 p-6 sm:flex-row">
        <center>
          <p className="text-3xl font-bold">
            Tech Stack Optimization Dashboard
          </p>
          <p>
            Results for{" "}
            <span className="font-mono font-thin">{repositoryName}</span>
          </p>
        </center>
      </div>

      <div className="chart-wrapper mx-auto flex max-w-6xl flex-col flex-wrap items-start justify-center gap-6 p-6 sm:flex-row sm:p-8">
        <div className="grid w-full flex-1 gap-6">
          <USimpleBlock
            value={monthlyCost}
            featureName={"Current Monthly Cost"}
          />
          <UServiceTable title={"Old Services"} tabularData={oldServices} />
          <UAiAssistant title={"AI Assistant"} description={aiAssistantResp} />
        </div>
        <div className="grid w-full flex-1 gap-6">
          <USimpleBlock
            value={newMonthlyCost}
            featureName={"New Monthly Cost"}
          />
          <UServiceTable title={"New Services"} tabularData={newServices} />

          <UCostComparisionBlock
            title={"Cost Comparison"}
            chartData={costComparisonData}
          />
        </div>
        {/* <div className="grid w-full flex-1 gap-6"> */}

        {/* <USimpleBlock value={serverUptime} featureName={"Server Uptime"} /> */}
        {/* <URevenueComparisionBlock title={"Comparison of Revenue"} /> */}
        {/* </div> */}
        <div className="grid w-full flex-1 gap-6">
          <USimpleBlock
            value={estimatedSavings}
            featureName={"Estimated Savings"}
          />
          <USimpleBlock
            value={currentTraffic}
            featureName={"Current Traffic"}
          />
          <USummaryBlock title={"Summary"} description={summary} />
          <UTrafficCostBlock title={"Traffic vs Cost"} />
        </div>
      </div>
    </main>
  );
}
