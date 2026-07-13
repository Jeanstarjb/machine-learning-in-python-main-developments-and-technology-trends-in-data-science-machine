import { Line } from 'react-chartjs-2';
import styled from 'styled-components';

const StatsContainer = styled.div`
  @apply grid grid-cols-1 md:grid-cols-3 gap-6 mb-8;
`;

const StatCard = styled.div`
  @apply bg-gradient-to-r from-indigo-500 to-purple-600 p-6 rounded-xl
    shadow-lg text-white transition-transform hover:scale-105;
`;

export default function Dashboard() {
  const data = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [{
      label: 'Model Performance',
      data: [65, 78, 82, 75, 88, 95],
      borderColor: '#6366f1',
      tension: 0.3,
      fill: false
    }]
  };

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">Analytics Dashboard</h1>
      <StatsContainer>
        <StatCard>
          <h3 className="text-lg font-semibold">Active Models</h3>
          <p className="text-4xl font-bold">24</p>
        </StatCard>
        <StatCard>
          <h3 className="text-lg font-semibold">Accuracy</h3>
          <p className="text-4xl font-bold">92.4%</p>
        </StatCard>
        <StatCard>
          <h3 className="text-lg font-semibold">Data Processed</h3>
          <p className="text-4xl font-bold">1.2M</p>
        </StatCard>
      </StatsContainer>
      <div className="bg-white p-6 rounded-xl shadow-sm">
        <Line data={data} />
      </div>
    </div>
  );
}
