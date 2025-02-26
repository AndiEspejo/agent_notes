'use client';

import React, { useEffect, useState } from 'react';
import { Document } from '@/types';
import { getDocuments } from '@/lib/api';

interface DocumentListProps {
  refreshTrigger: number;
}

export default function DocumentList({ refreshTrigger }: DocumentListProps) {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDocuments = async () => {
      setIsLoading(true);
      try {
        const data = await getDocuments();
        setDocuments(data);
        setError(null);
      } catch (err) {
        setError('Error loading documents. Please try again.');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDocuments();
  }, [refreshTrigger]);

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    else return (bytes / 1048576).toFixed(1) + ' MB';
  };

  const getFileIcon = (extension: string) => {
    switch (extension) {
      case '.pdf':
        return '📄';
      case '.docx':
      case '.doc':
        return '📝';
      default:
        return '📄';
    }
  };

  if (isLoading) {
    return (
      <div className='py-4 text-center text-gray-500'>Loading documents...</div>
    );
  }

  if (error) {
    return <div className='py-4 text-center text-red-500'>{error}</div>;
  }

  return (
    <div className='mt-2'>
      {documents.length === 0 ? (
        <div className='p-4 text-center bg-gray-50 rounded-lg text-gray-500'>
          No documents found. Upload your first document to get started!
        </div>
      ) : (
        <ul className='space-y-2'>
          {documents.map((doc, index) => (
            <li
              key={index}
              className='flex items-center p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors'
            >
              <span className='text-2xl mr-3'>
                {getFileIcon(doc.extension)}
              </span>
              <div className='flex-1 min-w-0'>
                <div className='font-medium text-gray-900 truncate'>
                  {doc.filename}
                </div>
                <div className='text-sm text-gray-500'>
                  {formatFileSize(doc.size)}
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
