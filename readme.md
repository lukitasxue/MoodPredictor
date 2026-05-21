## Dataset Variables

Each row in the training dataset corresponds to a single day of logged data, with the following features:

Variable Name	    Description	                                                                            Format / Range
sleep_hours	        Total number of hours slept the previous night.	                                        Numeric (e.g. 6.5)
stress_level	    Self-rated daily stress level. 1 = no stress, 10 = extremely stressed.	                Integer (1 to 10)
exercise_minutes	Total minutes of physical exercise done during the day.	                                Integer (e.g. 30)
nutrition_quality	Subjective quality of meals. 1 = poor (junk food), 5 = excellent (balanced).	        Integer (1 to 5)
social_minutes	    Time spent socializing (in person or online).	                                        Integer (minutes)
water_liters	    Total water consumed throughout the day.	                                            Numeric (liters, e.g. 2)
caffeine_cups	    Number of cups of coffee or other caffeinated drinks consumed.	                        Integer (e.g. 1, 2)
mood_score	        Target variable. Self-rated overall mood at end of day, from 1 (bad) to 10 (great).	    Numeric (1 to 10)
