/*
 Copyright (C) 2012 Bryan Maupin <bmaupincode@gmail.com>
 
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

/*
 Generates a password of a specified length given specific character classes
 
 Adapted mostly from:
 https://github.com/bmaupin/misc/blob/master/python/misc/pwgen.py
*/

function generatePassword() {
	// change these as necessary:
	// minimum password length
	var minPasswordLength = 8;
	// maximum password length
	var maxPasswordLength = 12;
	// minimum number of character classes
	var minClasses = 3;
	// character classes
    // l, I, 1, O, 0 removed for those who still haven't figured out how to copy and paste
	var charClasses = {"lower": "abcdefghijkmnopqrstuvwxyz",
                       "upper": "ABCDEFGHJKLMNPQRSTUVWXYZ",
                       "numbers": "23456789",
                       "symbols": "@#$%",
                       };
    // probabilities that a given character class will be used
    var classProbs = {"lower": 0.75,
    	              "upper": 0.05,
    	              "numbers": 0.1,
    	              "symbols": 0.1,
                      };

    function getRandomClass(classProbs) {
    	var names = new Array();
    	var weights = new Array();
    	var cumulativeWeight = 0;
    	var totalWeight = 0;

        // put these into arrays to ensure order is maintained
    	for (var name in classProbs) {
    	    names.push(name);
    	    weights.push(classProbs[name]);
    	}
        
        // calculate the total weight
        for (var i = 0; i < weights.length; i++) {
            totalWeight += weights[i];
        }
        var random = (Math.random() * totalWeight);

        for (i = 0; i < weights.length; i++) {
        	cumulativeWeight += weights[i];
        	if (random < cumulativeWeight) {
            	return names[i];
        	}
        }
    }

    function shuffle(array) {
        var tmp, current, top = array.length;

        if(top) while(--top) {
            current = Math.floor(Math.random() * (top + 1));
            tmp = array[current];
            array[current] = array[top];
            array[top] = tmp;
        }

        return array;
    }

    function buildPassword(passwordLength) {
        var charClass;
        var passwordChars = new Array();
        var usedClasses = new Array();
        
        // get all of the characters, leaving a few to make sure we get the minimum
        // number of classes
        for (var i = 0; i < passwordLength - minClasses; i++) {
        	charClass = getRandomClass(classProbs);
            if (usedClasses.indexOf(charClass) == -1) {
                usedClasses.push(charClass);
            }
            // get a random character from the character class
            passwordChars.push(charClasses[charClass].charAt(Math.floor(Math.random() * charClasses[charClass].length)));
        }
    
        // go through the last few characters
        for (var i = 0; i < minClasses; i++) {
            // if we haven't used the number of minimum classes
            if (usedClasses.length < minClasses) {
                // go through all the classes
                for (var charClass in charClasses) {
                    // find one we haven't used
                    if (usedClasses.indexOf(charClass) == -1) {
                        usedClasses.push(charClass);
                        break;
                    }
                }
            } else {
                // otherwise just get a random class
            	charClass = getRandomClass(classProbs);
            }
            // get a random character from the character class
            passwordChars.push(charClasses[charClass].charAt(Math.floor(Math.random() * charClasses[charClass].length)));
        }
    
        // now shuffle it all up for good measure
        passwordChars = shuffle(passwordChars);
        // and put it all together in a string
        return passwordChars.join("");
    }

    // use a random password length for more randomness
    return buildPassword(minPasswordLength + (Math.floor(Math.random() * (maxPasswordLength - minPasswordLength + 1))));    
}
