'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Message } from '@/types';
import { sendMessage } from '@/lib/api';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (input.trim() === '') return;

    const userMessage: Message = { text: input, sender: 'user' };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await sendMessage(input);

      setMessages((prevMessages) => [
        ...prevMessages,
        { text: response, sender: 'agent' },
      ]);
    } catch (error) {
      console.error('Error:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          text: 'Sorry, there was an error processing your request.',
          sender: 'agent',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className='flex flex-col h-full bg-white rounded-lg shadow-md overflow-hidden'>
      <div className='flex-1 p-4 overflow-y-auto'>
        {messages.length === 0 ? (
          <div className='flex flex-col items-center justify-center h-full text-center p-6 bg-gray-50 rounded-lg'>
            <h3 className='text-xl font-semibold text-blue-700 mb-2'>
              Welcome to your Study Agent!
            </h3>
            <p className='text-gray-600'>
              Ask questions about your documents or upload new materials to
              study.
            </p>
          </div>
        ) : (
          <div className='space-y-4'>
            {messages.map((message, index) => (
              <div
                key={index}
                className={`max-w-[80%] p-3 rounded-lg ${
                  message.sender === 'user'
                    ? 'ml-auto bg-blue-600 text-white rounded-br-sm'
                    : 'mr-auto bg-gray-100 text-gray-800 rounded-bl-sm'
                }`}
              >
                {message.text}
              </div>
            ))}
            {isLoading && (
              <div className='max-w-[80%] p-3 rounded-lg mr-auto bg-gray-100 text-gray-800 rounded-bl-sm'>
                <div className='flex space-x-1'>
                  <div
                    className='w-2 h-2 rounded-full bg-gray-500 animate-bounce'
                    style={{ animationDelay: '0ms' }}
                  ></div>
                  <div
                    className='w-2 h-2 rounded-full bg-gray-500 animate-bounce'
                    style={{ animationDelay: '150ms' }}
                  ></div>
                  <div
                    className='w-2 h-2 rounded-full bg-gray-500 animate-bounce'
                    style={{ animationDelay: '300ms' }}
                  ></div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <form
        className='p-4 border-t border-gray-200 flex'
        onSubmit={handleSubmit}
      >
        <Input
          type='text'
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder='Ask a question about your notes...'
          disabled={isLoading}
          className='flex-1 mr-2'
          fullWidth
        />
        <Button type='submit' disabled={isLoading || input.trim() === ''}>
          Send
        </Button>
      </form>
    </div>
  );
}
