import * as React from "react"
import { TooltipProps as RechartsTooltipProps } from "recharts/lib/component/Tooltip"

export interface ChartConfig {
  [key: string]: {
    label: string
    color: string
  }
}

interface ChartContainerProps {
  config: ChartConfig
  children: React.ReactNode
}

export function ChartContainer({ config, children }: ChartContainerProps) {
  return (
    <div className="chart-container" style={{ "--chart-1": "215 25% 27%", "--chart-2": "142 72% 29%" } as React.CSSProperties}>
      {React.Children.map(children, child => {
        if (React.isValidElement(child)) {
          const childProps = (child as React.ReactElement<any>).props;
          return React.cloneElement(child as React.ReactElement<any>, {
            style: {
              ...(childProps.style || {}),
              "--color-desktop": config.desktop?.color,
              "--color-mobile": config.mobile?.color,
            } as React.CSSProperties,
          })
        }
        return child
      })}
    </div>
  )
}

export function ChartTooltip(props: RechartsTooltipProps) {
  return <>{props.content}</>
}

export function ChartTooltipContent({ active, payload, label }: RechartsTooltipProps) {
  if (active && payload && payload.length) {
    return (
      <div className="rounded-lg border bg-background p-2 shadow-sm">
        <div className="grid grid-cols-2 gap-2">
          <div className="font-medium">{label}</div>
          {payload.map((entry: any) => (
            <div key={entry.name} className="flex items-center gap-1">
              <div className="h-2 w-2 rounded-full" style={{ backgroundColor: entry.color }} />
              <span>{entry.value}</span>
            </div>
          ))}
        </div>
      </div>
    )
  }
  return null
}

type TooltipProps<TValue, TName> = {
  active?: boolean;
  payload?: Array<{
    name: TName;
    value: TValue;
    payload?: any;
    dataKey?: string;
    color?: string;
  }>;
  label?: any;
}; 