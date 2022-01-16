
export const RabbitWeights = [ 'thin', 'normal', 'plump'          ] as const;
export const RabbitColors  = [ 'white', 'black', 'brown', 'green' ] as const;


export type RabbitWeight = typeof RabbitWeights[number];
export type RabbitColor  = typeof RabbitColors [number];


export interface Rabbit{
    id   ?: string;
    name ?: string;
    wool  : string;
    color : RabbitColor;
    weight: RabbitWeight;
}
