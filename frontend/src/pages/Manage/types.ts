export interface Transaction {
  id: number;
  category: string;
  amount: number;
  description: string;
  date: Date;
}

export type CreateTransaction = Omit<Transaction, 'id'>;

export interface TransactionFormFields {
  category: string;
  amount: string; // String because input values are strings until parsed
  description: string;
}
