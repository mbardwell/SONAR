input_pins=(P8.27 P8.28 P8.29 P8.30 P8.39 P8.40 P8.41 P8.42 P8.43 P8.44 P8.45 P8.46 P9.26)
output_pins=(P9.25 P9.27 P9.28 P9.29 P9.30 P9.31)

for pin in "${input_pins[@]}"
do
	config-pin -a $pin pruin
	config-pin -q $pin
done

for pin in "${output_pins[@]}"
do
	config-pin -a $pin pruout
	config-pin -q $pin
done 
