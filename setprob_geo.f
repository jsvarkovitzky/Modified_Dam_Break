c=========================================================================
      subroutine setprob
c=========================================================================

      use geoclaw_module
      use topo_module
      use dtopo_module

      implicit double precision (a-h,o-z)
      common /wave/ profile(202,8)

      call set_geo          !# sets basic parameters g and coord system
      call set_tsunami      !# sets parameters specific to tsunamis
      call set_topo         !# specifies topography (bathymetry) files
      call set_dtopo        !# specifies file with dtopo from earthquake
      call setqinit         !# specifies file with dh if this used instead
      call setregions       !# specifies where refinement is allowed/forced
      call setgauges        !# locations of measuring gauges
      call setfixedgrids    !# specifies output on arbitrary uniform fixed grids

      open(unit=76,file='../ts3c.txt',status='old',
     &     form='formatted')      

      do it=1,202 !this only reads in the first 10 seconds of data
         read(76,*) profile(it,1),profile(it,2),profile(it,3),
     &    profile(it,4), profile(it,5),profile(it,6),profile(it,7),
     &    profile(it,8)
      enddo
      
      !Shift time of BC and scale amplitude
      do it = 1,202
            profile(it,1) = profile(it,1)-265.05 !this is time in seconds
            profile(it,2) = profile(it,2)*1.0e0+0.218!this is amplitude in meters 
      end do 

      close(unit=76)

      return
      end
