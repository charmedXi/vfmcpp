#ifndef GUARD_FILAMENT_H
#define GUARD_FILAMENT_H

#include <vector>
#include <cmath>
#include <iostream>

using namespace std;

const double M_PI = 3.14159265359;

class Filament{
protected:
	int 						mN;
	vector <vector <double> > 	mPos;
	vector <vector <double> > 	mVel; 	// current velocity
	vector <vector <double> > 	mVel1;	// stores velocity last time step
	vector <vector <double> > 	mVel2;  // stores velocity 2 time steps ago
	vector <vector <double> >	mVelNL;
	vector <vector <double> > 	mSPrime;
	vector <vector <double> > 	mS2Prime;
	vector <double> 			mSegLengths;
public:
	Filament(){};
	~Filament(){};
	void CalcMeshLengths();
	void AdjMeshLengths(double dr);
	vector <double> GetMeshLengths(){return mSegLengths;}
	vector <vector <double> > GetSPrime(){return mSPrime;}
	vector <vector <double> > GetPos(){return mPos;}
	vector <vector <double> > GetVel(){return mVel;}
	int GetN(){return mN;}
	void CalcVelocity();
	void CalcSPrime();
	void CalcS2Prime();
	void CalcVelocitySelfNL();
	void CalcVelocityNL_OF(vector <vector <double> > PosOtherRing);
	void PropagatePosAB3(double & dt);
	//void PropagatePosRK4(double & dt);

};

class Ring : public Filament{
private:
	double 			mRadius0;
	vector <double>	mCentre;
public:
	Ring(){
		mRadius0 = 1e-6; 
		mN = 100;
		mCentre.resize(3,0);
		mPos.resize(mN); 
		for(int i=0; i<mN; i++){
			mPos[i].resize(3);
			mPos[i][0]=mCentre[0]+mRadius0*sin(i*(2*M_PI)/mN);
			mPos[i][1]=mCentre[1]+mRadius0*cos(i*(2*M_PI)/mN);
			mPos[i][2]=mCentre[2];
			if (i == mN - 1){
				mPos[i].push_back(3);
				mPos[i][3] = 0;
			}
			else{
				mPos[i].push_back(3);
				mPos[i][3] = i + 1;
			}
		}
		CalcMeshLengths();
	}
	Ring(double r, int N, double x, double y, double z){
		mRadius0 = r; mN = N;
		mCentre.resize(3);
		mCentre[0] = x; mCentre[1] = y; mCentre[2] = z;
		mPos.resize(mN);
		for(int i=0; i<mN; i++){
			mPos[i].resize(3);
			mPos[i][0]=mCentre[0]+mRadius0*sin(i*(2*M_PI)/mN);
			mPos[i][1]=mCentre[1]+mRadius0*cos(i*(2*M_PI)/mN);
			mPos[i][2]=mCentre[2];
			if (i == mN - 1){
				mPos[i].push_back(3);
				mPos[i][3] = 0;
			}
			else{
				mPos[i].push_back(3);
				mPos[i][3] = i + 1;
			}
		}
		CalcMeshLengths();
	}
};

#endif