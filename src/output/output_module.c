#include "output_module.h"

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void create_output(int program_type, long* checksums_array, cmd_line_args_t* args) {
    /* Name the file */
    char buffer[MAX_STRING_LENGTH];  // used to format ints to string
    char output_filename[MAX_LINE_LENGTH] = "results/";

    if (program_type == SERIAL) {
        strncat(output_filename, "serial_output_", MAX_STRING_LENGTH);
    } else if (program_type == PARALLEL) {
        strncat(output_filename, "parllel_output_", MAX_STRING_LENGTH);
    } else if (program_type == SERIAL_QUEUE) {
        strncat(output_filename, "serialqueue_output_", MAX_STRING_LENGTH);
    }
    // serial_output_n_T_W_counter

    strncat(output_filename, "n_", MAX_STRING_LENGTH);
    sprintf(buffer, "%d_", args->n);
    strncat(output_filename, buffer, MAX_STRING_LENGTH);

    strncat(output_filename, "T_", MAX_STRING_LENGTH);
    sprintf(buffer, "%d_", args->T);
    strncat(output_filename, buffer, MAX_STRING_LENGTH);

    strncat(output_filename, "W_", MAX_STRING_LENGTH);
    sprintf(buffer, "%d_", args->W);
    strncat(output_filename, buffer, MAX_STRING_LENGTH);

    sprintf(buffer, "%d.txt", args->trial_num);
    strncat(output_filename, buffer, MAX_STRING_LENGTH);

    remove(output_filename);
    FILE* output_file = fopen(output_filename, "a");
    if (output_file == NULL) {
        printf("Error opening output file");
        exit(1);
    }

    /* Write to file */
    for (int i = 0; i < args->numSources; i++) {
        char source_checksum[MAX_LINE_LENGTH] = "";

        sprintf(buffer, "%ld ", checksums_array[i]);  // used to format int (pos/neg) to string
        strncat(source_checksum, buffer, MAX_STRING_LENGTH);

        fputs(source_checksum, output_file);
        fputs("\n", output_file);
    }

    fclose(output_file);

    /* Clean up memory */
}