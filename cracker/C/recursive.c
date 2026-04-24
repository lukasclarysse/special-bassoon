#include <stdio.h>
#include <string.h>
#include <time.h>

const char *chars =
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789"
    "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~";

int found = 0;
long long attempts = 0;

void brute(char *target, char *guess, int depth, int max_len) {
    if (found) return;

    if (depth == max_len) {
        guess[depth] = '\0';
        attempts++;

        if (strcmp(guess, target) == 0) {
            found = 1;
            printf("Found: %s\n", guess);
        }
        return;
    }

    for (int i = 0; chars[i] != '\0'; i++) {
        guess[depth] = chars[i];
        brute(target, guess, depth + 1, max_len);
        if (found) return;
    }
}

int main() {
    char password[32];
    printf("Enter password: ");
    scanf("%31s", password);

    int len = strlen(password);
    char guess[32];

    clock_t start = clock();

    for (int l = 1; l <= len; l++) {
        brute(password, guess, 0, l);
        if (found) break;
    }

    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;

    printf("Attempts: %lld\n", attempts);
    printf("Time: %.4f seconds\n", time_spent);

    return 0;
}
