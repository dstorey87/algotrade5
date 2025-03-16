import React from 'react';

interface TestComponentProps {
  title: string;
}

export const TestComponent: React.FC<TestComponentProps> = ({ title }) => {
  return (
    <div className="p-4 bg-white rounded shadow">
      <h2 className="text-xl font-bold">{title}</h2>
      <p>Test component for pre-commit hook validation</p>
    </div>
  );
};