import React, { createContext, useContext, useState, ReactNode } from 'react';

interface TitleContextProps {
  title: string;
  setTitle: (title: string) => void;
}

interface TItleProviderProps {
    children: ReactNode
}

const TitleContext = createContext<TitleContextProps | undefined>(undefined);

export const TitleProvider: React.FC<TItleProviderProps> = ({ children }) => {
  const [title, setTitle] = useState<string>('Default Title');

  return (
    <TitleContext.Provider value={{ title, setTitle }}>
      {children}
    </TitleContext.Provider>
  );
};

export const useTitle = (): TitleContextProps => {
  const context = useContext(TitleContext);
  if (!context) {
    throw new Error('useTitle must be used within a TitleProvider');
  }
  return context;
};
