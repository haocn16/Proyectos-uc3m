# Import required dependencies
import numpy as np
import mdptoolbox

class ControlModule:
    def __init__(self):
        """ Dummy constructor to use the Python Class as a namespace """
        pass

    @staticmethod
    def generate_P(probabilities:np.ndarray, n_states:np.int32) -> np.ndarray:
        """ Function that generates the probabilities (transition) matrix """
        #matrix of transitions has dimension 3 actions x 100 current states x 100 next states
        p=np.zeros((3,n_states,n_states),dtype=np.float64)

        for state in range(n_states):
            #Action 0: decrease : -2,-1,0
            if state==0:
                #special case : state S0
                #for action 0 (decrease), starting at state 0, the probability of staying at state 0 is
                #probability in row 0 column 0 +probability in row 0 column 1 + probability in row 0 column 2
                p[0,state,0]=probabilities[0,0]+probabilities[0,1]+probabilities[0,2]
            elif state==1:
                #special case: state S1
                #for action 0 (decrease), starting at state 1, the probability of going to state 0 is
                #probability in row 0 column 0 +  probability in row 0 column 1
                p[0,state,0]=probabilities[0,0]+probabilities[0,1]
                #probability of staying at state 1 is: probability in row 0 column 2
                p[0,state,1]=probabilities[0,2]
            else:
                #general cases
                #for action 0 (decrease), starting at some state, the probability of going to state-2 is
                #probability in row 0 column 0
                p[0,state,state-2]=probabilities[0,0]
                #for action 0 (decrease), starting at some state, the probability of going to state-1 is
                #probability in row 0 column 1
                p[0,state,state-1]=probabilities[0,1]
                #for action 0 (decrease), starting at some state, the probability of staying in the same state is
                #probability in row 0 column 2
                p[0,state,state]=probabilities[0,2]
            
            #The same logic for the rest of actions: maintain and increase

            #Action 1: maintain (-1,0,+1)
            if state==0:
                #special case
                p[1,state,0]=probabilities[1,0]+probabilities[1,1]
                p[1,state,1]=probabilities[1,2]
            elif state==99:
                #special case
                p[1,state,98]=probabilities[1,0]
                p[1,state,99]=probabilities[1,1]+probabilities[1,2]
            else:
                #general cases
                p[1,state,state-1]=probabilities[1,0]
                p[1,state,state]=probabilities[1,1]
                p[1,state,state+1]=probabilities[1,2]
            
            #Action 2: increase (0,+1,+2)
            if state==99:
                #special case
                p[2,state,99]=probabilities[2,0]+probabilities[2,1]+probabilities[2,2]
            elif state==98:
                #special case
                p[2,state,98]=probabilities[2,0]
                p[2,state,99]=probabilities[2,1]+probabilities[2,2]
            else:
                #general cases
                p[2,state,state]=probabilities[2,0]
                p[2,state,state+1]=probabilities[2,1]
                p[2,state,state+2]=probabilities[2,2]
        #return the transition matrix p
        return p

    @staticmethod
    def generate_R(dt:np.float64, n_states:np.int32) -> np.ndarray:
        """ Function that generates the rewards (costs) matrix """
        #the cost matrix R has dimension 3 actions x 100 current states x 100 next states
        r=np.zeros((3,n_states,n_states),dtype=np.float64)
        
        for state in range(n_states):
            #divide it by 100 to get the value over 1
            current_power_level=state/100
            for state_prime in range (n_states):
                destination_power_level=state_prime/100
                cost=abs(dt-destination_power_level)

                #costs associated with actions that move away from the target must be multiplied by 2

                #action 0: decrease
                #if dt > current_power_level, apply penalty (multiplying by 2)
                if dt > current_power_level:
                    r[0,state,state_prime]=-(cost*2)
                else:
                    r[0,state,state_prime]=-cost
                
                #action 1: maintain
                #never move away from the goal
                r[1,state,state_prime]=-cost

                #action 2: increase
                #if dt < current_power_level, apply penalty (multiplying by 2)
                if dt < current_power_level:
                    r[2,state,state_prime]=-(cost*2)
                else:
                    r[2,state,state_prime]=-cost
        #return cost matrix
        return r
            
        

    @staticmethod
    def control_iteration(current_state:np.int32, dt:np.float64, probabilities:np.ndarray, n_states:np.int32,discount_factor:np.float64) -> np.int32:
        """ Function that computes one control-iteration """
        #That is, resolves which action (d,m,i) must be taken given a current demand (dt)
        #It builds the MDP from both matrices (p and r) and solves it using Value Iteration algorithm

        #generate matrix p for the MDP. It should receive the probabilities list and the number of states
        p=ControlModule.generate_P(probabilities,n_states)
        #generate matrix r for the MDP. It should receive the demand and the number of states
        r=ControlModule.generate_R(dt,n_states)

        #once generated, use the value iteration algorithm with the help pf mdptoolbox library
        value_iteration=mdptoolbox.mdp.ValueIteration(p,r,discount_factor)

        #execute the algorithm
        value_iteration.run()

        #value_iteration policy will return the best action for all states
        #we can take the action that corresponds to each state
        action=value_iteration.policy[current_state]

        #return the action to be taken
        return action

    @staticmethod
    def control_loop(demand: np.ndarray, 
                     probs: np.ndarray,
                     n_states: np.int32, 
                     n_actions: np.int32,
                     gamma: np.float64) -> np.ndarray:
        """ Function that computes all the required iterations (control-loop) to satisfy the power demand """
        #Some definitions
        #gamma = what we defined as discount_factor in control_iteration method
        #demand = what we defined as dt in control_iteration method
        #probs = what we defined as probabilities in control_iteration method

        #create a list to store the actual power level
        actual_power_level=np.zeros(len(demand))

        current_state=0

        #loop through every point in demand timeline
        for i in range(len(demand)):
            target=demand[i]
            #chose the action
            action=ControlModule.control_iteration(current_state,target,probs,n_states,gamma)

            #simulate the reactors
            if action==0:
                #decrease
                #use np.random as the instructions said
                behaviour=np.random.choice([-2,-1,0],p=probs[0])
            elif action==1:
                #maintain
                behaviour=np.random.choice([-1,0,1],p=probs[1])
            elif action==2:
                #increase
                behaviour=np.random.choice([0,1,2],p=probs[2])
            
            #apply the behaviour of the reactor to the current state
            current_state=current_state+behaviour

            #take into account the special cases:
            if current_state<0:
                current_state=0
            elif current_state>99:
                current_state=99
            
            #level power = state/100
            actual_power_level[i]=current_state/100

        #return the list
        return actual_power_level

