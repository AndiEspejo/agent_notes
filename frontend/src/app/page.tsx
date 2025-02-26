'use client';

import { useState } from 'react';
import Chat from '@/components/Chat';
import DocumentList from '@/components/DocumentList';
import DocumentUpload from '@/components/DocumentUpload';

export default function Home() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const refreshDocuments = () => {
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <main className='min-h-screen bg-gray-50'>
      <header className='bg-blue-700 text-white shadow-md'>
        <div className='container mx-auto py-4 px-6'>
          <h1 className='text-2xl font-bold'>Study Agent Interface</h1>
        </div>
      </header>

      <div className='container mx-auto p-6'>
        <div className='flex flex-col md:flex-row gap-6'>
          {/* Sidebar */}
          <div className='w-full md:w-1/3 lg:w-1/4'>
            <div className='bg-white rounded-lg shadow-md p-5 mb-6'>
              <h2 className='text-xl font-semibold text-blue-700 mb-4'>
                Upload Documents
              </h2>
              <DocumentUpload onUploadSuccess={refreshDocuments} />
            </div>

            <div className='bg-white rounded-lg shadow-md p-5'>
              <h2 className='text-xl font-semibold text-blue-700 mb-4'>
                Your Documents
              </h2>
              <DocumentList refreshTrigger={refreshTrigger} />
            </div>
          </div>

          {/* Chat section */}
          <div className='w-full md:w-2/3 lg:w-3/4'>
            <div className='bg-white rounded-lg shadow-md p-5 h-[calc(100vh-12rem)]'>
              <h2 className='text-xl font-semibold text-blue-700 mb-4'>
                Chat with your Study Agent
              </h2>
              <div className='h-[calc(100%-3rem)]'>
                <Chat />
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
