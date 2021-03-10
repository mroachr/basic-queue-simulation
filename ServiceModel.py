import random
import time
import csv
import numpy as np


class Simulation:
    def __init__(self):

        # settings
        self.capacity_service = 2
        self.capacity_queue = 5

        # initialize variables
        self.time = 0
        self.ID = 1
        self.lost_customers = 0
        self.t_arrival = self.generate_arrival()
        self.customers = {'customerID': [],
                          'inQueue': []}
        self.resources = {'resourceID': [i + 1 for i in range(self.capacity_service)],
                          'customerID': [0 for i in range(self.capacity_service)],
                          'isAvailable': [1 for i in range(self.capacity_service)],
                          't_service': [float('inf') for i in range(self.capacity_service)]}

    def advance_time(self):
        next_arrival = self.t_arrival
        next_service = min(self.resources['t_service'])
        next_event = min(next_arrival, next_service)
        self.time = next_event
        if next_event < next_arrival:
            self.handle_service(self.resources['t_service'].index(next_service))
        else:
            # if queue is maxed out, customer is lost --> "lost customer"
            if sum(self.customers['inQueue']) < self.capacity_queue:
                self.handle_arrival()
            else:
                self.lost_customers += 1
                self.t_arrival = self.time + self.generate_arrival()

    def handle_arrival(self):
        """Handles any instance of a new customer entering the system - Source"""

        # add new customer to system
        self.customers['customerID'].append(self.ID)
        self.customers['inQueue'].append(1)

        # attempt to get service right away
        self.move_customer(self.ID)

        # pull next arrival time-stamp
        self.t_arrival = self.time + self.generate_arrival()

        # iterate global customer ID counter
        self.ID += 1

    def handle_service(self, resource_i):
        """Handles any instance of a customer being serviced and then removed from the system - Sink"""

        # remove customer from system
        customer_i = self.customers['customerID'].index(self.resources['customerID'][resource_i])
        for key in self.customers.keys():
            del self.customers[key][customer_i]

        # update the resource's values
        self.resources['customerID'][resource_i] = 0
        self.resources['isAvailable'][resource_i] = 1
        self.resources['t_service'][resource_i] = float('inf')

        # try to pull a new customer from queue
        if sum(self.customers['inQueue']) > 0:
            next_customer_in_queue_ID = self.customers['customerID'][self.customers['inQueue'].index(1)]
            self.move_customer(next_customer_in_queue_ID)

    def move_customer(self, customerID):
        """Moves a targeted customer from queue position to an available resource for service"""

        # check if there is any available resources
        if sum(self.resources['isAvailable']) > 0:

            # update resource's values and status to taken
            resource_i = self.resources['isAvailable'].index(1)
            self.resources['customerID'][resource_i] = customerID
            self.resources['isAvailable'][resource_i] = 0
            self.resources['t_service'][resource_i] = self.time + self.generate_service()

            # update customer's values and status
            customer_i = self.customers['customerID'].index(customerID)
            self.customers['inQueue'][customer_i] = 0

    def generate_arrival(self):
        """Generates time until next arrival instance"""

        # Examples:
        # return round(np.random.exponential(0.5))  # Exponential probability density function (PDF)
        return random.randint(50, 200)

    def generate_service(self):
        """Generates time it takes to service/process a customer"""

        # Examples:
        # return np.random.poisson(1)  # poisson probability mass function (PMF)
        return random.randint(100, 500)


def runSim(seed=0, period=100, consoleFeedback=False, csvOutput=False):

    def toConsole():
        print('----------------------------------------------------')
        print('Current time:', sim.time)
        print('Customers:', sim.customers)
        print('Resources:', sim.resources)
        time.sleep(1)

    random.seed(seed)
    sim = Simulation()
    if csvOutput:
        with open('output.csv', 'w', newline='') as output:
            w = csv.writer(output, delimiter=';')
            w.writerow(['Time', 'Number of customers in queue'])
            w.writerow([sim.time, len(sim.customers['customerID'])])
            while sim.time < period:
                sim.advance_time()
                w.writerow([sim.time, len(sim.customers['customerID'])])
                if consoleFeedback:
                    toConsole()
    else:
        while sim.time < period:
            sim.advance_time()
            if consoleFeedback:
                toConsole()

runSim(seed=0, period=10000, consoleFeedback=False, csvOutput=True)






