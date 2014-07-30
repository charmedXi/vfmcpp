/* 	Adds or removes points to keep the resolution within a fixed range
Details given by Baggaley and Barenghi, PRB 83 (2011) */

#include "tangle.h"

using namespace std;

bool Tangle::MeshAdjust(){
	double dr = mDr;
	bool Remeshed = false;
	int AddCount = 0, DeleteCount = 0, N_p = 0;

	vector <Filament*>::iterator b, c, e;
	b = mTangle.begin(); e = mTangle.end();
	for(c=b;c!=e;c++){
		for (int k(0); k<(*c)->mN; k++){
			if(Remeshed==true){break;}
			/* maintain reasonable local curvature */
			double R(0); // 1/|s''| at new point
			for(int j(0);j!=3;j++){
				R += pow(((*c)->mPoints[k]->mNext->mS2Prime[j] + (*c)->mPoints[k]->mPrev->mS2Prime[j])/2,2);
			}
			R = sqrt(R);
			R = 1/R;
			/* point deletion for smoothing and proximity*/
			if((1/R)>1.9/dr || (*c)->mPoints[k]->mSegLength < 0.5*dr){
				AddCount++;	
			}
			/* point addition */
			else if ((*c)->mPoints[k]->mSegLength > dr){
				DeleteCount++;
			}
		}
	}

	if(DeleteCount >= 1 && AddCount >= 1){
		for(c=b;c!=e;c++){
			for (int k(0); k<(*c)->mN; k++){
				if(Remeshed==true){break;}
				/* maintain reasonable local curvature */
				double R(0); // 1/|s''| at new point
				for(int j(0);j!=3;j++){
					R += pow(((*c)->mPoints[k]->mNext->mS2Prime[j] + (*c)->mPoints[k]->mPrev->mS2Prime[j])/2,2);
				}
				R = sqrt(R);
				R = 1/R;
				/* point deletion for smoothing and proximity*/
				if((1/R)>1.9/dr || (*c)->mPoints[k]->mSegLength < 0.5*dr){
					if((1/R)>1.9/dr){cout << "Deleting point " << k << " / " << (*c)->mPoints.size() << " for smoothing." << endl;}
					if((*c)->mPoints[k]->mSegLength < 0.5*dr){cout << "Deleting point " << k << " / " << (*c)->mPoints.size() << " for proximity." << endl;}
					/* reassign next and last pointers for point to be deleted */
					(*c)->mPoints[k]->mNext->mPrev = (*c)->mPoints[k]->mPrev;
					(*c)->mPoints[k]->mPrev->mNext = (*c)->mPoints[k]->mNext;
					/* erase point from (*c)->mPoints and decrement mN */
					(*c)->mN--;
					delete (*c)->mPoints[k];
					(*c)->mPoints.erase((*c)->mPoints.begin()+k);
					(*c)->CalcMeshLengths(); (*c)->CalcSPrime(); (*c)->CalcS2Prime();
					break;
				}
				/* point addition */
				else if ((*c)->mPoints[k]->mSegLength > dr){
					cout << "Adding point at " << k << " / " <<  (*c)->mPoints.size() << endl;
					/* increment mN */
					(*c)->mN++;
					/* create new point and reassign pointers */
					(*c)->mPoints.push_back(new Point());
					(*c)->mPoints.back()->mPrev = (*c)->mPoints[k]->mPrev;
					(*c)->mPoints.back()->mNext = (*c)->mPoints[k];
					(*c)->mPoints[k]->mPrev->mNext = (*c)->mPoints.back();
					(*c)->mPoints[k]->mPrev = (*c)->mPoints.back();
					/* calculate position of new point a la PRB 2011, Baggaley & Barenghi */
					for(int j(0);j!=3;j++){
						(*c)->mPoints.back()->mS2Prime[j] = ((*c)->mPoints.back()->mNext->mS2Prime[j] + (*c)->mPoints.back()->mPrev->mS2Prime[j])/2;
						(*c)->mPoints.back()->mPos[j] = ((*c)->mPoints.back()->mS2Prime[j]) * R * (sqrt( pow(R,2) - 0.25*pow((*c)->mPoints.back()->mNext->mSegLength,2)) - R);
						(*c)->mPoints.back()->mPos[j] += 0.5*((*c)->mPoints.back()->mNext->mPos[j] + (*c)->mPoints.back()->mPrev->mPos[j]);
					}
					(*c)->CalcMeshLengths(); (*c)->CalcSPrime(); (*c)->CalcS2Prime();
					break;
				}
			}
		}
	}

	if(DeleteCount > 1 || AddCount > 1){
		return false;
	}

	return true;
	
	//if(Remeshed == true){MeshAdjust();}
}