'use client';

import React, { useState } from 'react';
import { uploadDocument } from '@/lib/api';
import Button from '@/components/ui/Button';

interface DocumentUploadProps {
  onUploadSuccess: () => void;
}

export default function DocumentUpload({
  onUploadSuccess,
}: DocumentUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setMessage(null);
      setError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    // Check file extension
    const fileExtension = file.name.split('.').pop()?.toLowerCase();
    if (!fileExtension || !['pdf', 'docx', 'doc'].includes(fileExtension)) {
      setError('Only PDF and Word documents (DOCX, DOC) are supported');
      return;
    }

    setUploading(true);
    setMessage(null);
    setError(null);

    try {
      const data = await uploadDocument(file);
      setMessage(data.message);
      setFile(null);

      if (onUploadSuccess) {
        onUploadSuccess();
      }

      const fileInput = document.getElementById(
        'file-upload'
      ) as HTMLInputElement;
      if (fileInput) fileInput.value = '';
    } catch (err) {
      const error = err as Error;
      setError(error.message);
      console.error('Upload error:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div className='mb-3'>
          <div className='relative'>
            <input
              type='file'
              id='file-upload'
              accept='.pdf,.docx,.doc'
              onChange={handleFileChange}
              disabled={uploading}
              className='absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10'
            />
            <div className='flex items-center justify-center px-4 py-6 border-2 border-dashed border-gray-300 rounded-lg text-center hover:bg-gray-50 transition-colors'>
              <div>
                <svg
                  className='mx-auto h-12 w-12 text-gray-400'
                  stroke='currentColor'
                  fill='none'
                  viewBox='0 0 48 48'
                  aria-hidden='true'
                >
                  <path
                    d='M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4h-8m-12 0H8m12 0v-8m12 8v-8'
                    strokeWidth='2'
                    strokeLinecap='round'
                    strokeLinejoin='round'
                  />
                </svg>
                <p className='mt-1 text-sm text-gray-500'>
                  {file ? file.name : 'Drag and drop a file or click to select'}
                </p>
              </div>
            </div>
          </div>
        </div>

        <Button type='submit' className='w-full' disabled={!file || uploading}>
          {uploading ? 'Uploading...' : 'Upload Document'}
        </Button>
      </form>

      {message && (
        <div className='mt-3 p-3 bg-green-50 text-green-700 rounded-md'>
          {message}
        </div>
      )}
      {error && (
        <div className='mt-3 p-3 bg-red-50 text-red-700 rounded-md'>
          {error}
        </div>
      )}

      <div className='mt-4 text-xs text-gray-500 space-y-1'>
        <p>Supported formats: PDF, DOCX</p>
        <p>Maximum file size: 10MB</p>
      </div>
    </div>
  );
}
