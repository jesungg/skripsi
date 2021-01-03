# from sklearn.metrics import mean_squared_error
predicted=[299, 578, 276, 132, 120, 91, 479, 524, 298, 355, 282, 261, 462, 387, 293, 284, 298, 318, 156, 299, 457, 104, 556, 418, 149, 60, 440, 38, 533, 573, 590, 272, 87, 457, 68, 113, 18, 412, 493, 94, 46, 438, 53, 193, 99, 8, 368, 412, 444, 511, 469, 589, 542, 447, 94, 138, 50, 528, 590, 413, 12, 453, 97, 174, 118, 74, 478, 102, 456, 414, 180, 44, 23, 528, 508, 266, 152, 9, 567, 393, 415, 385, 241, 295, 94, 28, 53, 526, 503, 9, 572, 380, 411, 375, 170, 44, 203, 225, 410, 417, 299, 459, 128, 385, 21, 121, 538, 299, 458, 127, 554, 82, 49, 115, 535, 572, 271, 458, 132, 481, 82, 53, 475, 115, 330, 350, 571, 582, 270, 526, 134, 455, 235, 48, 83, 117, 461, 488, 436, 410, 589, 491, 456, 556, 56, 134, 466, 368, 313, 119, 110, 204, 155, 58, 59, 226, 97, 6, 586, 532, 565, 264, 92, 401, 420, 132, 590, 6, 570, 465, 251, 171, 162, 333, 356, 375, 476, 20, 41, 477, 564, 111, 5, 574, 467, 287, 337, 377, 407, 478, 36, 4, 573, 550, 463, 399, 373, 135, 182, 455, 85, 34, 503, 562, 465, 359, 418, 403, 180, 99, 459, 506, 561, 545, 462, 406, 420, 177, 91, 163, 71, 453, 489, 351, 506, 563, 461, 407, 171, 92, 155, 351, 507, 560, 544, 461, 428, 169, 91, 163, 73, 452, 351, 487, 507, 559, 461, 408, 174, 20, 469, 6, 106, 130, 566, 402, 332, 374, 448, 158, 18, 469, 106, 5, 131, 372, 284, 332, 304, 157, 161, 164, 109, 5, 131, 170, 161, 164, 569, 370, 286, 138]
actual= [101.0, 58.0, 34.0, 261.0, 394.0, 367.0, 382.0, 361.0, 340.0, 391.0, 401.0, 383.0, 367.0, 359.0, 356.0, 317.0, 317.0, 348.0, 304.0, 353.0, 366.0, 334.0, 293.0, 317.0, 276.0, 313.0, 349.0, 383.0, 372.0, 340.0, 357.0, 325.0, 302.0, 271.0, 286.0, 307.0, 285.0, 261.0, 277.0, 255.0, 248.0, 233.0, 211.0, 222.0, 236.0, 251.0, 271.0, 286.0, 309.0, 327.0, 337.0, 320.0, 308.0, 290.0, 307.0, 326.0, 333.0, 312.0, 322.0, 308.0, 300.0, 289.0, 275.0, 287.0, 276.0, 286.0, 293.0, 287.0, 273.0, 259.0, 273.0, 285.0, 284.0, 277.0, 262.0, 278.0, 283.0, 289.0, 294.0, 291.0, 291.0, 282.0, 270.0, 259.0, 271.0, 281.0, 269.0, 282.0, 286.0, 291.0, 295.0, 289.0, 279.0, 276.0, 273.0, 279.0, 284.0, 285.0, 291.0, 285.0, 289.0, 278.0, 272.0, 282.0, 282.0, 289.0, 283.0, 293.0, 285.0, 276.0, 270.0, 280.0, 290.0, 289.0, 295.0, 289.0, 295.0, 288.0, 281.0, 287.0, 281.0, 283.0, 285.0, 294.0, 303.0, 302.0, 309.0, 304.0, 308.0, 306.0, 299.0, 292.0, 287.0, 292.0, 298.0, 302.0, 305.0, 313.0, 319.0, 323.0, 330.0, 322.0, 318.0, 322.0, 323.0, 323.0, 318.0, 313.0, 310.0, 306.0, 300.0, 294.0, 292.0, 287.0, 280.0, 288.0, 294.0, 300.0, 300.0, 294.0, 297.0, 300.0, 296.0, 303.0, 296.0, 303.0, 307.0, 305.0, 302.0, 299.0, 300.0, 301.0, 303.0, 307.0, 301.0, 295.0, 299.0, 305.0, 301.0, 294.0, 300.0, 304.0, 304.0, 305.0, 306.0, 308.0, 312.0, 306.0, 300.0, 306.0, 311.0, 314.0, 316.0, 318.0, 314.0, 312.0, 315.0, 310.0, 305.0, 309.0, 314.0, 317.0, 318.0, 320.0, 322.0, 319.0, 315.0, 318.0, 322.0, 327.0, 331.0, 334.0, 335.0, 337.0, 334.0, 330.0, 327.0, 323.0, 325.0, 329.0, 329.0, 333.0, 337.0, 339.0, 341.0, 338.0, 334.0, 331.0, 332.0, 335.0, 339.0, 343.0, 345.0, 347.0, 344.0, 340.0, 338.0, 333.0, 336.0, 336.0, 339.0, 342.0, 346.0, 348.0, 349.0, 347.0, 342.0, 344.0, 339.0, 335.0, 332.0, 336.0, 337.0, 338.0, 338.0, 340.0, 338.0, 333.0, 335.0, 332.0, 327.0, 324.0, 325.0, 325.0, 325.0, 325.0, 323.0, 320.0, 318.0, 315.0, 311.0, 308.0, 306.0, 304.0, 302.0, 306.0, 307.0, 307.0, 304.0]
# rms = mean_squared_error(y_actual, y_predicted, squared=False)
# print(rms)

from ml_metrics import rmse

rmse(actual, predicted)
print(rmse)
