import { render, screen, fireEvent } from '@testing-library/react';
import DatasetUpload from '../DatasetUpload';
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.post('/api/v1/datasets/upload', (req, res, ctx) => {
    return res(ctx.json({ location: 's3://bucket/test.csv' }));
  })
);

beforeAll(() => server.listen());
afterAll(() => server.close());

test('renders upload form and handles submission', async () => {
  render(<DatasetUpload />);
  
  const fileInput = screen.getByLabelText(/select file/i);
  const file = new File(['content'], 'test.csv', { type: 'text/csv' });
  fireEvent.change(fileInput, { target: { files: [file] } });
  
  fireEvent.click(screen.getByText(/upload dataset/i));
  
  await screen.findByText(/upload successful/i);
  expect(screen.getByText(/s3://bucket/test.csv/i)).toBeInTheDocument();
});
