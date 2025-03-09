declare module 'recharts' {
  export const CartesianGrid: any;
  export const Line: any;
  export const LineChart: any;
  export const XAxis: any;
  export const Tooltip: any;
  export const YAxis: any;
  export const Legend: any;
  export const ResponsiveContainer: any;
  export const Bar: any;
  export const BarChart: any;
  export const LabelList: any;
  export interface TooltipProps<TValue = any, TName = any> {
    active?: boolean;
    payload?: Array<{
      name: TName;
      value: TValue;
      payload?: any;
      dataKey?: string;
      color?: string;
    }>;
    label?: any;
  }
}

declare module 'recharts/lib/component/Tooltip' {
  export interface TooltipProps {
    active?: boolean;
    payload?: Array<any>;
    label?: any;
    content?: React.ReactNode;
    [key: string]: any;
  }
}

declare module 'recharts/lib/component/LabelList' {
  export const LabelList: any;
} 