export interface Message {
  text: string;
  sender: 'user' | 'agent';
}

export interface Document {
  filename: string;
  path: string;
  size: number;
  extension: string;
}
