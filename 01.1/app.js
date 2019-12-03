const fs = require('fs')

function getTotalFuelRequirementPromise(inputPath) {
    return new Promise((resolve) => {
        fs.readFile(inputPath, 'utf-8', (err, data) => {
            inputData = parseInputData(data);
            result = inputData.reduce((prev, current) => {
                return prev + fuelForMass(current);
            }, 0);
            resolve(result);
        });
    })
}

function parseInputData(inputData) {
    return inputData
        .split('\n')
        .filter(line => line.length > 0)
        .map(line => +line);
}

function fuelForMass(mass) {
    return Math.floor(mass / 3) - 2
}

getTotalFuelRequirementPromise('input.txt')
    .then(console.log)
