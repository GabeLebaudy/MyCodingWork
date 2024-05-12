#! /bin/bash

blacklist_arr=("_blacklist" "_special" "index.json")
special_arr=()
num_layers=-1

run_dir () {
   cd "$1"

   num_layers=$((num_layers+1))
   cur_files=()
   cur_dirs=()
   cur_special_files=()
   cur_special_dirs=()

   for file in *; do
      if [[ "$file" == "_blacklist" ]]; then
         fill_blacklist "$file"
      fi

      if [[ "$file" == "_special" ]]; then
         fill_special "$file"
      fi
   done
   
   for file in *; do
      if [[ -f "$file" ]]; then
         if check_arr "$file" "${blacklist_arr[@]}"; then
            :
         elif check_arr "$file" "${special_arr[@]}"; then
            cur_special_files+=("$file")
         else
            cur_files+=("$file")
         fi
      fi

      if [[ -d "$file" ]]; then
         if check_arr "$file" "${blacklist_arr[@]}"; then
            :
         elif check_arr "$file" "${special_arr[@]}"; then
            cur_special_dirs+=("$file")
         else
            cur_dirs+=("$file")
         fi
      fi
   done

   printf "{\n" > index.json

   write_json "files" "${cur_files[@]}"
   write_json "directories" "${cur_dirs[@]}"
   write_json "special_files" "${cur_special_files[@]}"
   write_json "special_directories" "${cur_special_dirs[@]}"

   printf " \"outer\": \"" >> index.json
   if [ $num_layers -eq 0 ]; then
      printf "\"\n" >> index.json
   elif [ $num_layers -eq 1 ]; then
      printf "..\"\n" >> index.json
   else
      for ((i = 0; i < $num_layers; i++)); do
         printf ".." >> index.json
         if [ $i -lt $(($num_layers - 1)) ]; then
            printf "/" >> index.json
         fi
      done
      printf "\"\n" >> index.json
   fi

   printf "}" >> index.json

   blacklist_arr=("_blacklist" "_special" "index.json")
   special_arr=()
   for file in *; do
      if [[ -d "$file" ]]; then
         run_dir "$file"
      fi
   done
   cd ".."
   num_layers=$((num_layers-1))
}

fill_blacklist () {
   while IFS= read -r line; do
      blacklist_arr+=("$line")
   done < $file
}

fill_special () {
   while IFS= read -r line; do
      special_arr+=("$line")
   done < $file
}

check_arr () {
   val="$1"
   arr=("${@:2}")
   for item in "${arr[@]}"; do
      if [[ "$val" == "$item" ]]; then
         return 0
      fi
   done
   return 1
}

write_json () {
   item="$1"
   arr=("${@:2}")

   printf " \"$item\": [" >> index.json
   if [ ${#arr[@]} -eq 0 ]; then
      :
   else
      for ((i = 0; i < ${#arr[@]}; i++)); do
         printf "\"${arr[i]}\"" >> index.json

         if [ $i -lt $((${#arr[@]} - 1)) ]; then
            printf ", " >> index.json
         fi
      done
   fi
   printf "],\n" >> index.json
}

if [[ -z $1 ]]; then
   echo "Error: Directory is a required argument."
   exit
fi

if [[ ! -d $1 ]]; then
   echo "Error: Argument provided is not a directory."
   exit
fi

run_dir "$1"