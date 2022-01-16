import React, { ReactElement, ReactNode } from 'react';
import ComponentAllert from '../../components/allert';
import FormControlSelect from '../../components/form/control/select';
import FormRange from '../../components/form/range';
import RabbitIcon                         from '../../components/rabbit';
import { RabbitsStore }                   from '../../storage';
import { Rabbit, RabbitColor, RabbitColors, RabbitWeight, RabbitWeights }                         from '../../storage/types';
import "./index.css";


export default class Page extends React.Component
{
  readonly state: {
    rabbits?: Rabbit[];
    bought ?: Rabbit[];
    error  ?: {
      type   : 'danger' | 'warning',
      message: string
    };
  } = { };

  async componentDidMount( )
  {
    try {
      const rabbits = await RabbitsStore.generate( 20, 40 );

      this.setState( { rabbits } );
    } catch ( error: unknown ) {
      this.setState( { error: { type: 'danger', message: `${error}` } } );
    }
  }
  
  protected renderRabbitContainer( rabbits: Rabbit[] ) : ReactNode
  {
    const bought = this.state.bought || [ ];

    return ( 
      <div>
        { rabbits.length > 0 && <h2> Market: {rabbits.length }</h2> }
        <div className="rabbit-container">
          { rabbits.map( ( rabbit, index ) => 
            <RabbitIcon color={rabbit.color} weight={rabbit.weight} key={rabbit.id || index}></RabbitIcon> ) }
        </div>
        <h2> You bought: { bought.length }</h2>
        <div className="rabbit-container-bought">
          { bought.map( ( rabbit, index ) => 
            <RabbitIcon color={rabbit.color} weight={rabbit.weight} key={rabbit.id || index}></RabbitIcon> ) }
        </div>
      </div> 
    );
  }

  async onSubmit( event: React.FormEvent )
  {
    event.preventDefault()

    const form = new FormData( event.target as HTMLFormElement );
    const data = Object.fromEntries( form );

    try {
      const result = await RabbitsStore.select( this.state.rabbits || [], data.color as RabbitColor, data.weight as RabbitWeight, data.limit as string );

      this.setState( { rabbits: result.remaining, bought: [ ...( this.state.bought || [ ]), ...result.selected ] } );
    } catch ( error: unknown ) {
      this.setState( { error: { type: 'warning', message: `${error}` } } )
    }
  }

  protected renderPrefference( maxRabbitRange: number ) 
  {
      const minRange = maxRabbitRange >= 6 ? 6:maxRabbitRange;
      
      return ( <form className="prefferences-container" onSubmit={ event => this.onSubmit( event ) }>
        <h3>Prefferences</h3>
        < hr/>
        <FormControlSelect name="weight" label="Weight" value="plump" options={RabbitWeights.map( value => { return { title: value, value } } )}/>
        <FormControlSelect name="color"  label="Color"  options={RabbitColors .map( value => { return { title: value, value } } )}/>
        <FormRange         name="limit"  label="Count"  value={minRange} min={minRange} max={maxRabbitRange}/>
        <br />
        <button type="submit" className="btn btn-dark">Buy</button>
    </form> );
  }

  render( ) : ReactElement
  {
    const error = this.state.error;

    if ( error && error.type === "danger" )
    {
      return <ComponentAllert {...error}/>;
    }

    return (  <div className="container">
      { error && <ComponentAllert {...error}/>}
      <br/>
      { this.state.rabbits && this.renderRabbitContainer( this.state.rabbits ) }
      < hr/>
      { this.state.rabbits && this.state.rabbits.length > 0 && this.renderPrefference( this.state.rabbits.length ) }
    </div> )
  }
} 