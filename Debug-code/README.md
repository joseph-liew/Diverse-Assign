# Notes
-	*Debug-code* is identical to the *Main-code*. But with additional lines added to trace important steps. Useful for debugging or understanding how the *Main-code* works.
-	To print / output the debugging traces, uncomment at the start of the *Helper Functions*:
>> - The function definition *debug_print(message: str, variable, debug_flag: bool)*
>> - Enable tracing by uncommenting *debug-flag* variable. Set *debug-flag* to TRUE for tracing. Set to FALSE to skip tracing.
- Elsewhere in the rest of the code, uncomment any *debug_print( )* calls to enable tracing. Note: tracing will not be printed / outputted unless *debug_flag* is set to TRUE
