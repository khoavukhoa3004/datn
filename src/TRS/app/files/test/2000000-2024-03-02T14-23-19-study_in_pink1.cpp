#include "study_in_pink1.h"

bool readFile(
    const string &filename,
    int &HP1,
    int &HP2,
    int &EXP1,
    int &EXP2,
    int &M1,
    int &M2,
    int &E1,
    int &E2,
    int &E3)
{
    // This function is used to read the input file,
    // DO NOT MODIFY THIS FUNTION
    ifstream ifs(filename);
    if (ifs.is_open())
    {
        ifs >> HP1 >> HP2 >> EXP1 >> EXP2 >> M1 >> M2 >> E1 >> E2 >> E3;
        return true;
    }
    else
    {
        cerr << "The file is not found" << endl;
        return false;
    }
}

////////////////////////////////////////////////////////////////////////
/// STUDENT'S ANSWER BEGINS HERE
/// Complete the following functions
/// DO NOT modify any parameters in the functions.
////////////////////////////////////////////////////////////////////////

void modify_hp(int &h)
{
    if (h < 0)
        h = 0;
    else if (h > 666)
        h = 666;
}

void modify_exp(int &ex)
{
    if (ex < 0)
        ex = 0;
    else if (ex > 600)
        ex = 600;
}

void modify_money(int &mo)
{
    if (mo < 0)
        mo = 0;
    else if (mo > 3000)
        mo = 3000;
}

int roundUp(float num)
{
    if (num - int(num) > 0)
        return int(num) + 1;
    return int(num);
}

int check3consec(string s)
{
    for (int i = 0; i < s.size() - 2; i++)
    {
        if (s[i] == s[i + 1] == s[i + 2])
            return i;
    }
    return -1;
}

bool checkSpecial(string s)
{
    for (int i = 0; i < s.size(); i++)
    {
        if (s[i] == '@' || s[i] == '#' || s[i] == '%' || s[i] == '$' || s[i] == '!')
            return true;
    }
    return false;
}

int checkOtherChar(string s)
{
    for (int i = 0; i < s.size(); i++)
    {
        if (s[i] != '@' && s[i] != '#' && s[i] != '%' && s[i] != '$' && s[i] != '!' && !('a' <= s[i] && s[i] <= 'z') && !('A' <= s[i] && s[i] <= 'Z') && !('0' <= s[i] && s[i] <= '9'))
            return i;
    }
    return -1;
}

int nearestSquare(int num)
{
    float a = sqrt(num);
    if (a - int(a) == 0)
        return num;
    else
    {
        int a1 = int(a) * int(a);
        int a2 = (int(a) + 1) * (int(a) + 1);
        if (num - a1 < a2 - num)
            return a1;
        else
            return a2;
    }
}

int findMaxinArr(int arr[10][10], int i, int j)
{

    int iTemp = i, jTemp = j;
    int maxVal = arr[i][j];

    //  I TĂNG, J TĂNG
    while (iTemp <= 9 && jTemp <= 9)
    {
        if (arr[iTemp][jTemp] > maxVal)
            maxVal = arr[iTemp][jTemp];
        iTemp++;
        jTemp++;
    }
    iTemp = i, jTemp = j;
    //  I GIẢM, J GIẢM
    while (iTemp >= 0 && jTemp >= 0)
    {
        if (arr[iTemp][jTemp] > maxVal)
            maxVal = arr[iTemp][jTemp];
        iTemp--;
        jTemp--;
    }
    iTemp = i, jTemp = j;
    //  I TĂNG, J GIẢM
    while (iTemp <= 9 && jTemp >= 0)
    {
        if (arr[iTemp][jTemp] > maxVal)
            maxVal = arr[iTemp][jTemp];
        iTemp++;
        jTemp--;
    }
    iTemp = i, jTemp = j;
    //  I GIẢM, J TĂNG
    while (iTemp >= 0 && jTemp <= 9)
    {
        if (arr[iTemp][jTemp] > maxVal)
            maxVal = arr[iTemp][jTemp];
        iTemp--;
        jTemp++;
    }
    if (maxVal >= 0)
        return maxVal;
    else
        return -maxVal;
}
// Task 1 - XONG
int firstMeet(int &exp1, int &exp2, int e1)
{
    // TODO: Complete this function
    if (e1 < 0 || e1 > 99)
        return -99;
    if (0 <= e1 && e1 <= 3)
    { // TH1
        if (e1 == 0)
            exp2 += 29;
        else if (e1 == 1)
            exp2 += 45;
        else if (e1 == 2)
            exp2 += 75;
        else
            exp2 += (29 + 45 + 75);
        modify_exp(exp2);

        int d = e1 * 3 + exp1 * 7;
        if (d % 2 == 0)
        {
            float temp = exp1 + d * 1.0 / 200;
            exp1 = roundUp(temp);
        }
        else
        {
            float temp = exp1 - d * 1.0 / 100;
            exp1 = roundUp(temp);
        }
        modify_exp(exp1);
    }
    else // TH2
    {
        if (4 <= e1 && e1 <= 19)
        { // Thông tin 1
            float temp = exp2 + e1 * 1.0 / 4 + 19;
            exp2 = roundUp(temp);
        }
        else if (20 <= e1 && e1 <= 49)
        { // Thông tin 2
            float temp = exp2 + e1 * 1.0 / 9 + 21;
            exp2 = roundUp(temp);
        }
        else if (50 <= e1 && e1 <= 65)
        { // Thông tin 3
            float temp = exp2 + e1 * 1.0 / 16 + 17;
            exp2 = roundUp(temp);
        }
        else if (66 <= e1 && e1 <= 79)
        {
            float temp = exp2 + e1 * 1.0 / 4 + 19;
            exp2 = roundUp(temp);
            if (exp2 > 200)
            {
                temp = exp2 + e1 * 1.0 / 9 + 21;
                exp2 = roundUp(temp);
            }
        }
        else
        {
            float temp = exp2 + e1 * 1.0 / 4 + 19;
            exp2 = roundUp(temp);
            temp = exp2 + e1 * 1.0 / 9 + 21;
            exp2 = roundUp(temp);
            if (exp2 > 400)
            {
                temp = exp2 + e1 * 1.0 / 16 + 17;
                exp2 = roundUp(temp);
                temp = exp2 * 1.15;
                exp2 = roundUp(temp);
            }
        }
        modify_exp(exp2);
        exp1 -= e1;
    }
    return exp1 + exp2;
}

// Task 2 - XONG
int traceLuggage(int &HP1, int &EXP1, int &M1, int E2)
{
    // TODO: Complete this function
    if (E2 < 0 || E2 > 99)
        return -99;
    float p1, p2, p3;
    //  PATH 1
    int S = nearestSquare(EXP1);
    if (EXP1 >= S)
        p1 = 1.0;
    else
        p1 = (EXP1 * 1.0 / S + 80) / 123;

    //  PATH 2
    if (E2 % 2 == 0)
    {
        float temp;
        //  ACTION 1
        if (HP1 < 200)
        {
            temp = HP1 * 1.3;
            HP1 = roundUp(temp);
            M1 -= 150;
        }
        else
        {
            temp = HP1 * 1.1;
            HP1 = roundUp(temp);
            M1 -= 70;
        }
        if (M1 < 0)
        {
            modify_money(M1);
            goto End;
        }
        //  ACTION 2
        if (EXP1 < 400)
            M1 -= 200;
        else
            M1 -= 120;
        temp = EXP1 * 1.13;
        EXP1 = roundUp(temp);
        if (M1 < 0)
        {
            modify_money(M1);
            goto End;
        }
        //  ACTION 3
        if (EXP1 < 300)
            M1 -= 100;
        else
            M1 -= 120;
        temp = EXP1 * 0.9;
        EXP1 = roundUp(temp);
        if (M1 < 0)
        {
            modify_money(M1);
            goto End;
        }
    }
    else
    {
        float needToPay = 0.0;
        int M1First = M1;
        while (needToPay <= M1First / 2)
        {
            float temp;
            //  ACTION 1
            if (HP1 < 200)
            {
                temp = HP1 * 1.3;
                HP1 = roundUp(temp);
                M1 -= 150;
                needToPay += 150;
            }
            else
            {
                temp = HP1 * 1.1;
                HP1 = roundUp(temp);
                M1 -= 70;
                needToPay += 70;
            }
            if (M1 < 0 || needToPay > M1First / 2)
            {
                modify_money(M1);
                goto End;
            }
            //  ACTION 2
            if (EXP1 < 400)
            {
                M1 -= 200;
                needToPay += 200;
            }
            else
            {
                M1 -= 120;
                needToPay += 120;
            }
            temp = EXP1 * 1.13;
            EXP1 = roundUp(temp);
            if (M1 < 0 || needToPay > M1First / 2)
            {
                modify_money(M1);
                goto End;
            }
            //  ACTION 3
            if (EXP1 < 300)
            {
                M1 -= 100;
                needToPay += 100;
            }
            else
            {
                M1 -= 120;
                needToPay += 120;
            }
            temp = EXP1 * 0.9;
            EXP1 = roundUp(temp);
            if (M1 < 0 || needToPay > M1First / 2)
            {
                modify_money(M1);
                goto End;
            }
        }
    }
End:
    HP1 = roundUp(HP1 * 0.83);
    EXP1 = roundUp(EXP1 * 1.17);
    S = nearestSquare(EXP1);
    if (EXP1 >= S)
        p2 = 1.0;
    else
        p2 = (EXP1 * 1.0 / S + 80) / 123;

    //  PATH 3
    int arrP[10] = {32, 47, 28, 79, 100, 50, 22, 83, 64, 11};
    if (E2 < 10)
        p3 = arrP[E2] / 10;
    else
    {
        int idx = E2 / 10 + E2 % 10;
        p3 = arrP[idx] / 10;
    }

    // FINISH ALL 3 PATH

    if (p1 + p2 + p3 == 3.0)
    {
        float temp = EXP1 * 0.75;
        EXP1 = roundUp(temp);
        modify_exp(EXP1);
    }
    else
    {
        float aver = (p1 + p2 + p3) / 3;
        float temp;
        if (aver < 0.5)
        {
            temp = HP1 * 0.85;
            HP1 = roundUp(temp);
            temp = EXP1 * 1.15;
            EXP1 = roundUp(temp);
        }
        else
        {
            temp = HP1 * 0.9;
            HP1 = roundUp(temp);
            temp = EXP1 * 1.2;
            EXP1 = roundUp(temp);
        }
        modify_exp(EXP1);
        modify_hp(HP1);
    }
    return HP1 + EXP1 + M1;
}

// Task 3 - XONG
int chaseTaxi(int &HP1, int &EXP1, int &HP2, int &EXP2, int E3)
{
    // TODO: Complete this function
    if (E3 < 0 || E3 > 99)
        return -99;
    int arrTaxi[10][10], arrSher[10][10];
    for (int i = 0; i < 10; i++)
    {
        for (int j = 0; j < 10; j++)
        {
            arrTaxi[i][j] = ((E3 * j) + (i * 2)) * (i - j);
            arrSher[i][j] = 0;
        }
    }

    for (int i = 0; i < 10; i++)
    {
        for (int j = 0; j < 10; j++)
        {
            arrSher[i][j] = findMaxinArr(arrTaxi, i, j);
        }
    }

    int iMeet = 0, jMeet = 0;
    for (int i = 0; i < 10; i++)
    {
        for (int j = 0; j < 10; j++)
        {
            if (arrTaxi[i][j] > E3 * 2)
                iMeet++;
            if (arrTaxi[i][j] < -E3)
                jMeet++;
        }
    }

    while (iMeet >= 10)
    {
        iMeet = iMeet % 10 + iMeet / 10;
    }
    while (jMeet >= 10)
    {
        jMeet = jMeet % 10 + jMeet / 10;
    }
    float temp;
    if (abs(arrTaxi[iMeet][jMeet]) <= arrSher[iMeet][jMeet]) // ĐUỔI KỊP TAXI
    {
        temp = EXP1 * 1.12;
        EXP1 = roundUp(temp);
        temp = EXP2 * 1.12;
        EXP2 = roundUp(temp);
        temp = HP1 * 1.1;
        HP1 = roundUp(temp);
        temp = HP2 * 1.1;
        HP2 = roundUp(temp);
        modify_exp(EXP1);
        modify_exp(EXP2);
        modify_hp(HP1);
        modify_hp(HP2);
        return arrSher[iMeet][jMeet];
    }
    else // KHÔNG ĐUỔI KỊP TAXI
    {
        temp = EXP1 * 0.88;
        EXP1 = roundUp(temp);
        temp = EXP2 * 0.88;
        EXP2 = roundUp(temp);
        temp = HP1 * 0.9;
        HP1 = roundUp(temp);
        temp = HP2 * 0.9;
        HP2 = roundUp(temp);
        modify_exp(EXP1);
        modify_exp(EXP2);
        modify_hp(HP1);
        modify_hp(HP2);
        return arrTaxi[iMeet][jMeet];
    }
}

// Task 4 - XONG
int checkPassword(const char *s, const char *email)
{
    // TODO: Complete this function
    string se = "";
    int cnt = 0;
    while (email[cnt] != '@')
    {
        se += email[cnt++];
    }
    string pass = "";
    cnt = 0;
    while (s[cnt] != '\0')
    {
        pass += s[cnt++];
    }
    if (pass.size() < 8) // < MIN SIZE
        return -1;
    else if (pass.size() > 20) // > MAX SIZE
        return -2;
    else if (checkOtherChar(pass) != -1) //  CONTAIN OTHER SPECIAL CHAR
        return checkOtherChar(pass);
    else if (pass.find(se) >= 0 && pass.find(se) < pass.size()) // CONTAIN SE
        return -(300 + pass.find(se));
    else if (check3consec(pass) != -1) // CONTAIN 3 CONSECUTIVE SIMILAR CHAR
        return -(400 + check3consec(pass));
    else if (!checkSpecial(pass)) // NOT CONTAIN SPECIAL CHAR
        return -5;
    else // ACCEPTABLE
        return -10;
}

// Task 5 - XONG
int findCorrectPassword(const char *arr_pwds[], int num_pwds)
{
    // TODO: Complete this function
    string maxFreq;
    int numFreq = 0, cnt = 0;
    bool check = false;
    pair<string, int> arr[35];
    for (int i = 0; i < num_pwds; i++)
    {
        for (int j = 0; j < cnt; j++)
        {
            if (arr[j].first == arr_pwds[i])
            {
                arr[j].second++;
                check = true;
                break;
            }
        }
        if (check)
        {
            check = false;
            continue;
        }
        else
        {
            arr[cnt++] = {arr_pwds[i], 1};
        }
    }
    for (int i = 0; i < cnt; i++)
    {
        if (arr[i].second >= numFreq)
        {
            if (arr[i].second == numFreq)
            {
                if (arr[i].first.size() > maxFreq.size())
                {
                    maxFreq = arr[i].first;
                }
            }
            else
            {
                maxFreq = arr[i].first;
                numFreq = arr[i].second;
            }
        }
    }
    int finalAns;
    for (int i = 0; i < num_pwds; i++)
    {
        if (arr_pwds[i] == maxFreq)
        {
            finalAns = i;
            break;
        }
    }
    return finalAns;
}

////////////////////////////////////////////////
/// END OF STUDENT'S ANSWER
////////////////////////////////////////////////