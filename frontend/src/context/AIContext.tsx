import React, { createContext, useContext, useState, useRef } from 'react';
import apiClient from '../api/client';
import toast from 'react-hot-toast';

const AIContext = createContext<any>(null);

export const AIProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [query, setQuery] = useState('');
  const [advice, setAdvice] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);

  const handleStop = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
      setLoading(false);
      setAdvice(null);
      toast.error('Neural Analysis Terminated', { icon: '🛑' });
    }
  };

  const askAI = async (explicitQuery?: string) => {
    const finalQuery = explicitQuery || query;
    if (loading || !finalQuery.trim()) return;

    setLoading(true);
    setAdvice(null);

    // Initialize a new controller for this specific request
    const controller = new AbortController();
    abortControllerRef.current = controller;

    try {
      const response = await apiClient.get('/ai/advice', {
        params: { query: finalQuery },
        signal: controller.signal,
      });

      setAdvice(response.data.advice);

      const isOnAIPage = window.location.pathname === '/ai-advisor';
      toast.success(isOnAIPage ? 'Analysis Synchronized' : 'Strategic Insight Ready in Advisor', {
        icon: '🧠',
      });
    } catch (err: any) {
      // Check if the error was caused by our handleStop() call
      if (err.name === 'CanceledError' || err.code === 'ERR_CANCELED') {
        console.log('Neural link intentionally severed');
      } else {
        toast.error('AI Core Offline');
        setAdvice('System was unable to reach the neural network.');
      }
    } finally {
      setLoading(false);
      abortControllerRef.current = null;
    }
  };

  return (
    <AIContext.Provider value={{ query, setQuery, advice, setAdvice, loading, askAI, handleStop }}>
      {children}
    </AIContext.Provider>
  );
};

export const useAI = () => useContext(AIContext);
