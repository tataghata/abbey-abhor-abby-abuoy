#include <cmath>
#include <cstdint>
#include <vector>
#include <algorithm>
static inline float clamp(float x,float a,float b){return std::min(std::max(x,a),b);}
static void shade(const float *v, float *c){
 float nx=v[3],ny=v[4],nz=v[5];float il=1.f/std::sqrt(nx*nx+ny*ny+nz*nz);nx*=il;ny*=il;nz*=il;
 const float lights[3][7]={{-.405f,.579f,.707f,1.05f,1.f,.923f,.82f},{.795f,.159f,.585f,.35f,.68f,.76f,1.f},{-.318f,-.848f,.424f,.32f,.91f,.66f,1.f}};
 for(int ch=0;ch<3;ch++)c[ch]=v[6+ch]*(.085f+.04f*std::max(ny,0.f));
 for(int k=0;k<3;k++){
 const float *l=lights[k];float nd=std::max(nx*l[0]+ny*l[1]+nz*l[2],0.f);
 float hx=l[0],hy=l[1],hz=l[2]+1;float hl=1.f/std::sqrt(hx*hx+hy*hy+hz*hz);float nh=std::max((nx*hx+ny*hy+nz*hz)*hl,0.f);
 float spec=.40f*std::pow(nh,38.f)+.16f*std::pow(nh,180.f);
 for(int ch=0;ch<3;ch++)c[ch]+=(v[6+ch]*nd+spec)*l[3]*l[4+ch];
 }
 float fres=std::pow(1.f-clamp(nz,0,1),3.f)*.055f;
 for(int ch=0;ch<3;ch++){c[ch]+=fres; c[ch]=255.f*std::sqrt(clamp(c[ch]/(1.f+.28f*c[ch]),0.f,1.f));}
}
extern "C" void render(const float *tri,int count,int W,int H,float scale,uint8_t *out){
 std::vector<float> depth((size_t)W*H,-1.e20f);
 for(int ti=0;ti<count;ti++){
 const float *a=tri+ti*27,*b=a+9,*c=b+9;
 float ax=a[0]*scale+W*.5f,ay=H*.5f-a[1]*scale,bx=b[0]*scale+W*.5f,by=H*.5f-b[1]*scale,cx=c[0]*scale+W*.5f,cy=H*.5f-c[1]*scale;
 float area=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy);if(std::abs(area)<.00001f)continue;
 int x0=std::max(0,(int)std::floor(std::min({ax,bx,cx}))),x1=std::min(W-1,(int)std::ceil(std::max({ax,bx,cx})));
 int y0=std::max(0,(int)std::floor(std::min({ay,by,cy}))),y1=std::min(H-1,(int)std::ceil(std::max({ay,by,cy})));
 if(x0>x1||y0>y1)continue;
 float ca[3],cb[3],cc[3];shade(a,ca);shade(b,cb);shade(c,cc);
 float inv=1.f/area;float dax=(by-cy)*inv,day=(cx-bx)*inv,dbx=(cy-ay)*inv,dby=(ax-cx)*inv;
 for(int y=y0;y<=y1;y++){
 float wa=((by-cy)*(x0+.5f-cx)+(cx-bx)*(y+.5f-cy))*inv;
 float wb=((cy-ay)*(x0+.5f-cx)+(ax-cx)*(y+.5f-cy))*inv;
 for(int x=x0;x<=x1;x++,wa+=dax,wb+=dbx){float wc=1-wa-wb;if(wa<-.000001f||wb<-.000001f||wc<-.000001f)continue;float z=wa*a[2]+wb*b[2]+wc*c[2];size_t p=(size_t)y*W+x;if(z<=depth[p])continue;depth[p]=z;for(int ch=0;ch<3;ch++)out[p*4+ch]=(uint8_t)clamp(wa*ca[ch]+wb*cb[ch]+wc*cc[ch],0,255);out[p*4+3]=255;}
 }
 }
}
