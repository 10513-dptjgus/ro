import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";

const data = [
  // 연령별 인구수 데이터 예시 (각 연령대별로 상위 5개 지역의 인구수)
  { age: "0세", 경기도: 90000, 서울특별시: 41000, 부산광역시: 12000, 경상남도: 13000, 인천광역시: 11000 },
  { age: "1세", 경기도: 87000, 서울특별시: 37500, 부산광역시: 11500, 경상남도: 12500, 인천광역시: 10500 },
  { age: "2세", 경기도: 89000, 서울특별시: 39100, 부산광역시: 11800, 경상남도: 12800, 인천광역시: 10800 },
  // ... 연령대별로 이어서 전체 데이터 입력 필요
];

export default function AgePopulationChart() {
  return (
    <div className="w-full max-w-5xl mx-auto p-4">
      <h2 className="text-xl font-bold mb-4 text-center">2025년 5월 상위 5개 지역 연령별 인구 분포</h2>
      <ResponsiveContainer width="100%" height={500}>
        <LineChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="age" />
          <YAxis />
          <Tooltip formatter={(value) => value.toLocaleString()} />
          <Legend />
          <Line type="monotone" dataKey="경기도" stroke="#1e90ff" strokeWidth={2} />
          <Line type="monotone" dataKey="서울특별시" stroke="#ff4d4f" strokeWidth={2} />
          <Line type="monotone" dataKey="부산광역시" stroke="#82ca9d" strokeWidth={2} />
          <Line type="monotone" dataKey="경상남도" stroke="#ffc658" strokeWidth={2} />
          <Line type="monotone" dataKey="인천광역시" stroke="#a28dd0" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
