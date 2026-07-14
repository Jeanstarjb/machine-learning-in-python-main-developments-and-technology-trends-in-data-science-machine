import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styled from 'styled-components';
import { Line } from 'react-chartjs-2';
import { CircularProgress } from '@mui/material';

const Container = styled.div`
  padding: 2rem;
  background: #f9fafb;
  min-height: 100vh;
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  font-weight: bold;
  color: #1f2937;
`;

const UploadSection = styled.div`
  background: #ffffff;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
`;

const FileInput = styled.input`
  margin-top: 1rem;
`;

const ChartContainer = styled.div`
  background: #ffffff;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
`;

const Dashboard = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [chartData, setChartData] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/api/data/upload/csv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Upload successful:', response.data);
      fetchChartData();
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setUploading(false);
    }
  };

  const fetchChartData = async () => {
    try {
      const response = await axios.get('/api/evaluation/metrics');
      const { labels, data } = response.data;
      setChartData({
        labels,
        datasets: [
          {
            label: 'Model Performance',
            data,
            borderColor: '#4f46e5',
            backgroundColor: 'rgba(79, 70, 229, 0.2)',
            tension: 0.4,
          },
        ],
      });
    } catch (error) {
      console.error('Failed to fetch chart data:', error);
    }
  };

  useEffect(() => {
    fetchChartData();
  }, []);

  return (
    <Container>
      <Header>
        <Title>ML Platform Dashboard</Title>
      </Header>

      <UploadSection>
        <h2>Upload Dataset</h2>
        <FileInput type="file" onChange={handleFileChange} />
        <button
          onClick={handleUpload}
          disabled={uploading}
          style={{
            marginTop: '1rem',
            padding: '0.5rem 1rem',
            background: '#4f46e5',
            color: '#ffffff',
            border: 'none',
            borderRadius: '0.5rem',
            cursor: 'pointer',
          }}
        >
          {uploading ? <CircularProgress size={20} color="inherit" /> : 'Upload'}
        </button>
      </UploadSection>

      {chartData && (
        <ChartContainer>
          <h2>Model Performance</h2>
          <Line data={chartData} />
        </ChartContainer>
      )}
    </Container>
  );
};

export default Dashboard;